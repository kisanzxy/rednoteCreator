"""
Task definitions for the Rednote Virality Agents crew.
"""

from crewai import Task
from src.agents import create_trend_scout, create_strategist, create_creator


def create_scraping_task(trend_scout, topic: str) -> Task:
    """
    Task for Trend Scout to scrape Rednote posts.
    """
    return Task(
        description=(
            f"Search Xiaohongshu (Rednote) for posts related to the topic: '{topic}'. "
            "Use the Rednote Scraper tool to find and scrape the top 5 viral posts. "
            "For each post, collect:\n"
            "- Post title\n"
            "- Image URL\n"
            "- Top 3 comments\n"
            "\n"
            "Save all the data to a CSV file and provide a summary of what was scraped, "
            "including the CSV file path."
        ),
        agent=trend_scout,
        expected_output=(
            "A summary text containing:\n"
            "1. Number of posts scraped\n"
            "2. CSV file path where data is saved\n"
            "3. Brief overview of each scraped post (title, URL, key comments)"
        )
    )


def create_analysis_task(strategist, topic: str) -> Task:
    """
    Task for Strategist to analyze scraped data.
    """
    return Task(
        description=(
            f"Analyze the scraped Rednote data for the topic '{topic}'. "
            "Read the CSV file provided by the Trend Scout and identify:\n"
            "1. Viral hooks - What makes these posts engaging?\n"
            "2. Keyword patterns - Common words/phrases that appear in viral content\n"
            "3. User sentiment - How do users react to these posts (based on comments)?\n"
            "4. Content structure - What format/structure do viral posts follow?\n"
            "5. Emotional triggers - What emotions do these posts evoke?\n"
            "\n"
            "Provide a comprehensive analysis explaining WHY these posts worked and "
            "what patterns can be replicated for new content."
        ),
        agent=strategist,
        expected_output=(
            "A detailed text brief (2-3 paragraphs) explaining:\n"
            "- Key viral hooks identified\n"
            "- Keyword and content patterns\n"
            "- User sentiment analysis\n"
            "- Recommendations for creating similar viral content"
        )
    )


def create_content_creation_task(creator, topic: str) -> Task:
    """
    Task for Creator to write new post variations.
    """
    return Task(
        description=(
            f"Based on the Strategist's analysis, create 3 new post variations for the topic '{topic}' "
            "in authentic Xiaohongshu (Little Red Book) style.\n\n"
            "Each post must include:\n"
            "1. A clickbait-style title with brackets, e.g., [Must See] or [Hot Topic]\n"
            "2. Heavy use of emojis (✨🔥👇💕🌟💯 etc.)\n"
            "3. Bullet points or numbered lists\n"
            "4. Engaging, conversational tone\n"
            "5. Relevant hashtags at the end\n"
            "6. Content that follows the viral patterns identified by the Strategist\n\n"
            "Make sure each variation is unique but follows the same successful patterns. "
            "The content should feel authentic to Rednote users and have high viral potential."
        ),
        agent=creator,
        expected_output=(
            "Three complete post variations, each formatted as:\n"
            "\n"
            "--- Post Variation 1 ---\n"
            "[Title with brackets]\n"
            "\n"
            "[Content with emojis, bullet points, and engaging text]\n"
            "\n"
            "#hashtag1 #hashtag2 #hashtag3\n"
            "\n"
            "[Repeat for Post Variations 2 and 3]"
        )
    )
