"""
Main entry point for Rednote Virality Agents.
Orchestrates the CrewAI workflow to scrape, analyze, and create Rednote content.

Note: Import warnings may appear until dependencies are installed via:
    pip install -r requirements.txt
"""

import os
from dotenv import load_dotenv  
from crewai import Crew, Process 
from langchain_openai import ChatOpenAI  
from langchain_google_genai import ChatGoogleGenerativeAI 

from src.agents import create_trend_scout, create_strategist, create_creator
from src.tasks import create_scraping_task, create_analysis_task, create_content_creation_task


def get_llm():
    """
    Initialize and return the appropriate LLM based on environment configuration.
    """
    load_dotenv()
    
    provider = os.getenv('LLM_PROVIDER', 'openai').lower()
    
    if provider == 'gemini':
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY or GOOGLE_API_KEY not found in .env file. "
                "Please set GEMINI_API_KEY or switch to OpenAI."
            )
        # Set environment variable for langchain-google-genai
        os.environ['GOOGLE_API_KEY'] = api_key
        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7
        )
    else:  # Default to OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in .env file. "
                "Please set OPENAI_API_KEY in your .env file."
            )
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            api_key=api_key
        )


def main():
    """
    Main execution function.
    """
    print("=" * 60)
    print("Rednote Virality Agents - Content Creation System")
    print("=" * 60)
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Get user input
    topic = input("Enter the topic you want to analyze and create content for: ").strip()
    
    if not topic:
        print("Error: Topic cannot be empty.")
        return
    
    print(f"\nStarting analysis for topic: '{topic}'")
    print("This may take a few minutes...\n")
    
    try:
        # Initialize LLM
        llm = get_llm()
        print(f"Using LLM provider: {os.getenv('LLM_PROVIDER', 'openai')}\n")
        
        # Create agents
        print("Creating agents...")
        trend_scout = create_trend_scout(llm)
        strategist = create_strategist(llm)
        creator = create_creator(llm)
        
        # Create tasks
        print("Setting up tasks...")
        scraping_task = create_scraping_task(trend_scout, topic)
        analysis_task = create_analysis_task(strategist, topic)
        content_task = create_content_creation_task(creator, topic)
        
        # Set up task dependencies
        analysis_task.context = [scraping_task]
        content_task.context = [analysis_task]
        
        # Create crew
        print("Assembling crew...\n")
        crew = Crew(
            agents=[trend_scout, strategist, creator],
            tasks=[scraping_task, analysis_task, content_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute crew
        print("=" * 60)
        print("Starting crew execution...")
        print("=" * 60)
        print()
        
        result = crew.kickoff()
        
        # Display results
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
        # Save results to file
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)
        result_file = os.path.join(output_dir, f"result_{topic.replace(' ', '_')}.txt")
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"Topic: {topic}\n")
            f.write("=" * 60 + "\n\n")
            f.write(str(result))
        
        print(f"\nResults also saved to: {result_file}")
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease ensure:")
        print("1. You have created a .env file with your API key")
        print("2. Set either OPENAI_API_KEY or GEMINI_API_KEY")
        print("3. Optionally set LLM_PROVIDER to 'openai' or 'gemini'")
    except Exception as e:
        print(f"\nError during execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
