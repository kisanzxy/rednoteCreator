"""
Custom tools for CrewAI agents.
Contains the RednoteScraperTool for scraping Xiaohongshu (Rednote) content.
"""

import asyncio
import json
import os
import pandas as pd
from typing import Type
from bs4 import BeautifulSoup
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler


class RednoteScraperInput(BaseModel):
    """Input schema for RednoteScraperTool."""
    topic: str = Field(..., description="The search topic/keyword to scrape Rednote for")


class RednoteScraperTool(BaseTool):
    """
    Tool for scraping Xiaohongshu (Rednote) posts based on a search topic.
    Scrapes top 5 posts including titles, images, and top 3 comments.
    """
    name: str = "Rednote Scraper"
    description: str = (
        "Scrapes Xiaohongshu (Rednote) for viral posts related to a given topic. "
        "Returns a CSV file path and summary of scraped data including titles, images, and comments."
    )
    args_schema: Type[BaseModel] = RednoteScraperInput

    def _run(self, topic: str) -> str:
        """
        Synchronous entry point for CrewAI tool.
        Wraps async scraping logic.
        """
        try:
            return asyncio.run(self._scrape_rednote(topic))
        except Exception as e:
            return f"Error during scraping: {str(e)}"

    async def _scrape_rednote(self, topic: str) -> str:
        """
        Main async scraping logic.
        """
        # Load cookies
        cookies_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "xhs_cookies.json")
        if not os.path.exists(cookies_path):
            return (
                f"Error: xhs_cookies.json not found at {cookies_path}. "
                "Please create this file with your Xiaohongshu login cookies. "
                "See xhs_cookies.json.example for format."
            )

        try:
            with open(cookies_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
        except Exception as e:
            return f"Error loading cookies: {str(e)}"

        # Convert cookies to format expected by crawl4ai
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']

        # Construct search URL
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={topic}"
        
        # Prepare output directory
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        scraped_data = []

        try:
            async with AsyncWebCrawler(verbose=False) as crawler:
                # JavaScript code to scroll and load content
                js_code = """
                // Scroll down to load more content
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(resolve => setTimeout(resolve, 2000));
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(resolve => setTimeout(resolve, 2000));
                return document.body.innerHTML;
                """

                # Crawl search results page
                result = await crawler.arun(
                    url=search_url,
                    cookies=cookie_dict,
                    js_code=js_code,
                    wait_for="body"
                )

                if not result.success:
                    return f"Failed to crawl search page: {result.error_message}"

                # Parse HTML to find post URLs
                soup = BeautifulSoup(result.html, 'html.parser')
                post_urls = []

                # Look for /explore/ links
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    if '/explore/' in href:
                        full_url = href if href.startswith('http') else f"https://www.xiaohongshu.com{href}"
                        if full_url not in post_urls:
                            post_urls.append(full_url)
                            if len(post_urls) >= 5:
                                break

                # If we didn't find enough URLs, try alternative selectors
                if len(post_urls) < 5:
                    # Try finding links with explore in the path
                    for link in soup.find_all('a'):
                        href = link.get('href', '')
                        if 'explore' in href.lower():
                            full_url = href if href.startswith('http') else f"https://www.xiaohongshu.com{href}"
                            if full_url not in post_urls:
                                post_urls.append(full_url)
                                if len(post_urls) >= 5:
                                    break

                # Scrape individual posts
                for i, post_url in enumerate(post_urls[:5], 1):
                    try:
                        post_result = await crawler.arun(
                            url=post_url,
                            cookies=cookie_dict,
                            wait_for="body"
                        )

                        if not post_result.success:
                            scraped_data.append({
                                'post_number': i,
                                'url': post_url,
                                'title': 'Content unavailable',
                                'image_url': 'Content unavailable',
                                'comments': 'Content unavailable'
                            })
                            continue

                        post_soup = BeautifulSoup(post_result.html, 'html.parser')
                        
                        # Extract title
                        title = 'Content unavailable'
                        title_selectors = ['.title', '#detail-title', 'h1', '[class*="title"]', 'title']
                        for selector in title_selectors:
                            try:
                                title_elem = post_soup.select_one(selector)
                                if title_elem:
                                    title = title_elem.get_text(strip=True)
                                    if title:
                                        break
                            except:
                                continue
                        
                        if not title or title == 'Content unavailable':
                            # Fallback: try meta title
                            meta_title = post_soup.find('meta', property='og:title')
                            if meta_title:
                                title = meta_title.get('content', 'Content unavailable')

                        # Extract image URL
                        image_url = 'Content unavailable'
                        og_image = post_soup.find('meta', property='og:image')
                        if og_image:
                            image_url = og_image.get('content', 'Content unavailable')
                        else:
                            # Fallback: try to find any image
                            img_tag = post_soup.find('img')
                            if img_tag and img_tag.get('src'):
                                image_url = img_tag.get('src')
                                if not image_url.startswith('http'):
                                    image_url = f"https://www.xiaohongshu.com{image_url}"

                        # Extract top comments
                        comments = []
                        comment_selectors = [
                            '[class*="comment"]',
                            '[class*="Comment"]',
                            '.comment-item',
                            '[data-testid*="comment"]'
                        ]
                        
                        for selector in comment_selectors:
                            try:
                                comment_elems = post_soup.select(selector)[:3]
                                for elem in comment_elems:
                                    comment_text = elem.get_text(strip=True)
                                    if comment_text and len(comment_text) > 5:
                                        comments.append(comment_text)
                                if len(comments) >= 3:
                                    break
                            except:
                                continue

                        # If no comments found, try generic text extraction
                        if not comments:
                            # Look for any divs/spans that might contain comments
                            all_text_elements = post_soup.find_all(['div', 'span', 'p'])
                            for elem in all_text_elements[:20]:  # Limit search
                                text = elem.get_text(strip=True)
                                if text and 10 < len(text) < 200:  # Reasonable comment length
                                    if text not in comments:
                                        comments.append(text)
                                        if len(comments) >= 3:
                                            break

                        comments_str = ' | '.join(comments[:3]) if comments else 'No comments found'

                        scraped_data.append({
                            'post_number': i,
                            'url': post_url,
                            'title': title,
                            'image_url': image_url,
                            'comments': comments_str
                        })

                    except Exception as e:
                        scraped_data.append({
                            'post_number': i,
                            'url': post_url,
                            'title': f'Error: {str(e)}',
                            'image_url': 'Content unavailable',
                            'comments': 'Content unavailable'
                        })

        except Exception as e:
            return f"Error during scraping process: {str(e)}"

        # Save to CSV
        if scraped_data:
            df = pd.DataFrame(scraped_data)
            csv_filename = f"scraped_data_{topic.replace(' ', '_')}.csv"
            csv_path = os.path.join(output_dir, csv_filename)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')

            # Create summary
            summary = f"Successfully scraped {len(scraped_data)} posts for topic '{topic}'.\n"
            summary += f"CSV file saved to: {csv_path}\n\n"
            summary += "Summary of scraped posts:\n"
            for item in scraped_data:
                summary += f"\nPost {item['post_number']}:\n"
                summary += f"  Title: {item['title'][:100]}...\n" if len(item['title']) > 100 else f"  Title: {item['title']}\n"
                summary += f"  URL: {item['url']}\n"
                summary += f"  Comments: {item['comments'][:150]}...\n" if len(item['comments']) > 150 else f"  Comments: {item['comments']}\n"

            return f"{summary}\n\nCSV file path: {csv_path}"
        else:
            return f"No data scraped for topic '{topic}'. Please check your cookies and network connection."
