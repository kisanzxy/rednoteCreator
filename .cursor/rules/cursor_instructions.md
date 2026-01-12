This instruction file enforces the architecture we discussed: **CrewAI + Crawl4AI + Local Execution**.

***

# Project Specification: Rednote Virality Agents

## 1. Project Context
We are building a local, multi-agent workflow using **CrewAI**. The goal is to accept a user topic, scrape **Rednote (Xiaohongshu)** for viral posts and comments using **Crawl4AI**, analyze the data for trends, and generate new content in the specific "Rednote Style."

## 2. Tech Stack Requirements
*   **Python:** 3.10+
*   **Orchestration:** `crewai` (Latest version)
*   **LLM:** `openai` (GPT-4o) or `google-generativeai` (Gemini). Use `.env` for keys.
*   **Scraping:** `crawl4ai` (Async web crawler).
*   **Browser Automation:** `playwright` (Required by crawl4ai).
*   **Data Handling:** `pandas` (for CSV handling), `BeautifulSoup4` (for HTML parsing).

## 3. Architecture & Agents
The system must run locally without a UI initially.

### Agents
1.  **Trend Scout (Researcher):**
    *   **Goal:** Search Rednote, scrape top 5 posts, grab titles/images/top 3 comments.
    *   **Tool:** Custom `RednoteScraperTool`.
    *   **Output:** A CSV file path and a summary of the data.
2.  **The Strategist (Analyst):**
    *   **Goal:** Analyze the scraped data (CSV). Find "viral hooks," keyword patterns, and user sentiment.
    *   **Input:** The data provided by the Scout.
    *   **Output:** A text brief on *why* these posts worked.
3.  **The Creator (Copywriter):**
    *   **Goal:** Write 3 new post variations based on the Strategist's insights.
    *   **Style:** Heavy emojis, "Little Red Book" aesthetic, clickbait titles, specific hashtag usage.

## 4. Implementation Steps (Cursor Instructions)

### Step 1: File Structure
Generate the following folder structure:
```text
rednote-crew/
├── .env                # API Keys (OPENAI_API_KEY, GEMINI_API_KEY)
├── xhs_cookies.json    # User-provided login cookies (manual setup)
├── requirements.txt    # Dependencies
├── src/
│   ├── main.py         # Entry point
│   ├── tools.py        # Custom Crawl4AI tool logic
│   ├── agents.py       # Agent definitions
│   └── tasks.py        # Task definitions
└── output/             # Folder for CSVs and results
```

### Step 2: Tool Implementation (`src/tools.py`)
Create a custom tool class `RednoteScraperTool(BaseTool)` compatible with CrewAI.
*   **Important:** CrewAI tools run synchronously, but `crawl4ai` is asynchronous. You must wrap the `crawl4ai` logic inside `asyncio.run()`.
*   **Logic:**
    1.  Load `xhs_cookies.json`. If missing, return a helpful error.
    2.  Construct search URL: `https://www.xiaohongshu.com/search_result?keyword={topic}`.
    3.  Use `AsyncWebCrawler` with `js_code` to scroll down and load content.
    4.  Extract post URLs (look for `/explore/` links).
    5.  Visit individual post URLs to scrape:
        *   Title (try selectors like `.title`, `#detail-title`).
        *   Image URL (`og:image` meta tag).
        *   Top Comments (class names vary, try generic text extraction from comment containers).
    6.  Save data to `output/scraped_data_{topic}.csv`.

### Step 3: Agents & Tasks (`src/agents.py`, `src/tasks.py`)
*   Define the 3 agents with distinct `backstory` and `goals`.
*   **Strategist** should not use tools; it purely processes the text from the previous step.
*   **Creator** should have a prompt emphasizing "Little Red Book" formatting (bullet points, emojis like ✨🔥👇, and bracketed titles like [Must See]).

### Step 4: Execution (`src/main.py`)
*   Use `dotenv` to load keys.
*   Instantiate `Crew` with `Process.sequential`.
*   Ask user for input: `topic = input("Enter topic: ")`.
*   Kickoff the crew.

## 5. Coding Rules for Cursor
1.  **Error Handling:** The scraper is fragile. Wrap scraping logic in `try/except` blocks. If specific CSS selectors fail, fallback to getting `body` text or return "Content unavailable" rather than crashing.
2.  **Cookies:** Assume `xhs_cookies.json` is a list of dictionaries (standard EditThisCookie format).
3.  **Dependencies:** Ensure `requirements.txt` includes: `crewai`, `crawl4ai`, `playwright`, `beautifulsoup4`, `pandas`, `python-dotenv`.
4.  **Async/Sync Bridge:** Be careful with the event loop. The Tool `_run` method is the entry point; inside it, call the async crawler.

---

### How to use this with Cursor:

1.  Open Cursor.
2.  Press **Cmd + I** (or Ctrl + I) to open **Composer**.
3.  Paste the content above into the input box.
4.  Hit **Generate**.
5.  Cursor will create the file structure and write the code.
6.  **Manual Step:** You will still need to manually create the `xhs_cookies.json` file (login to Rednote in Chrome, use an extension to export cookies to JSON) and put it in the root folder.