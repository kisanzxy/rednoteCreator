"""
Agent definitions for the Rednote Virality Agents crew.
"""

from crewai import Agent
from src.tools import RednoteScraperTool


def create_trend_scout(llm) -> Agent:
    """
    Trend Scout (Researcher Agent)
    Searches Rednote and scrapes top viral posts.
    """
    return Agent(
        role='Trend Scout',
        goal='Search Xiaohongshu (Rednote) for viral posts related to the given topic, '
             'scrape the top 5 posts including titles, images, and top 3 comments, '
             'and save the data to a CSV file.',
        backstory=(
            "You are an expert researcher specializing in social media trend analysis, "
            "particularly on Xiaohongshu (Rednote). You have a keen eye for identifying "
            "viral content and understand what makes posts popular. Your job is to "
            "thoroughly search and collect data on trending posts related to any given topic."
        ),
        tools=[RednoteScraperTool()],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_strategist(llm) -> Agent:
    """
    The Strategist (Analyst Agent)
    Analyzes scraped data to identify viral hooks and patterns.
    """
    return Agent(
        role='The Strategist',
        goal='Analyze the scraped Rednote data to identify viral hooks, keyword patterns, '
             'user sentiment, and explain why these posts became popular.',
        backstory=(
            "You are a data analyst and content strategist with years of experience "
            "decoding viral content patterns. You excel at finding hidden patterns in "
            "social media data, understanding user psychology, and identifying what makes "
            "content shareable. You read CSV files and extract insights that help create "
            "winning content strategies."
        ),
        tools=[],  # Strategist doesn't use tools, only processes text/CSV data
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_creator(llm) -> Agent:
    """
    The Creator (Copywriter Agent)
    Writes new post variations in Rednote style.
    """
    return Agent(
        role='The Creator',
        goal='Write 3 new post variations based on the Strategist\'s insights, '
             'following the authentic Xiaohongshu (Little Red Book) style with heavy emojis, '
             'clickbait titles, and proper hashtag usage.',
        backstory=(
            "You are a master copywriter specializing in Xiaohongshu (Little Red Book) content. "
            "You understand the unique aesthetic and style of Rednote posts: bullet points, "
            "emojis like ✨🔥👇💕, bracketed titles like [Must See], and the perfect balance "
            "of informative and engaging content. You create content that feels authentic to "
            "the platform and has high viral potential."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
