# Rednote Virality Agents

A multi-agent AI system built with CrewAI that scrapes Xiaohongshu (Rednote/小红书) for viral posts, analyzes trends, and generates new content in authentic Rednote style.

## 🎯 Project Overview

This system uses three specialized AI agents working together:

1. **Trend Scout** - Searches and scrapes top 5 viral posts from Rednote
2. **The Strategist** - Analyzes scraped data to identify viral hooks and patterns
3. **The Creator** - Generates 3 new post variations in authentic Rednote style

## 🛠️ Tech Stack

- **Python:** 3.10+
- **Orchestration:** CrewAI
- **LLM:** OpenAI GPT-4o or Google Gemini
- **Scraping:** Crawl4AI with Playwright
- **Data Handling:** Pandas, BeautifulSoup4

## 📋 Prerequisites

- Python 3.10 or higher
- A Xiaohongshu (Rednote) account (for cookies)
- OpenAI API key OR Google Gemini API key

## 🚀 Setup Instructions

### 1. Clone and Navigate

```bash
cd redNoteCreator
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

Crawl4AI requires Playwright browsers:

```bash
playwright install
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai

# OR for Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here
LLM_PROVIDER=gemini
```

### 6. Set Up Xiaohongshu Cookies

You need to export your Xiaohongshu login cookies to authenticate scraping:

1. Log in to [Xiaohongshu](https://www.xiaohongshu.com) in your browser
2. Use a browser extension like "EditThisCookie" or "Cookie-Editor" to export cookies
3. Save the cookies as `xhs_cookies.json` in the root directory
4. See `xhs_cookies.json.example` for the expected format

**Important:** The cookies file should be a JSON array of cookie objects with at least:
- `domain`: ".xiaohongshu.com"
- `name`: cookie name (e.g., "sessionid", "web_session")
- `value`: cookie value
- `path`: "/"
- `secure`: true/false
- `httpOnly`: true/false

## 🏃 Usage

Run the main script:

```bash
python src/main.py
```

The system will:
1. Prompt you for a topic/keyword
2. Scrape top 5 viral posts related to that topic
3. Analyze the posts for viral patterns
4. Generate 3 new post variations in Rednote style

### Output Files

- **CSV Data:** `output/scraped_data_{topic}.csv` - Contains scraped post data
- **Results:** `output/result_{topic}.txt` - Contains final analysis and generated content

## 📁 Project Structure

```
redNoteCreator/
├── .env                    # API keys (create this)
├── .gitignore             # Git ignore rules
├── xhs_cookies.json       # Your cookies (create this)
├── xhs_cookies.json.example  # Cookie format example
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/
│   ├── main.py          # Entry point
│   ├── tools.py         # RednoteScraperTool implementation
│   ├── agents.py        # Agent definitions
│   └── tasks.py         # Task definitions
└── output/              # Generated CSV and result files
```

## 🔧 How It Works

1. **Trend Scout** uses the `RednoteScraperTool` to:
   - Search Xiaohongshu for the given topic
   - Scrape top 5 posts (titles, images, comments)
   - Save data to CSV

2. **The Strategist** analyzes the CSV to identify:
   - Viral hooks and engagement patterns
   - Keyword trends
   - User sentiment
   - Content structure patterns

3. **The Creator** generates 3 post variations with:
   - Clickbait titles with brackets [Must See]
   - Heavy emoji usage (✨🔥👇💕)
   - Bullet points and lists
   - Relevant hashtags
   - Authentic Rednote style

## ⚠️ Important Notes

- **Cookies Required:** The scraper needs valid Xiaohongshu login cookies to work
- **Rate Limiting:** Be respectful of Xiaohongshu's servers. Don't run too many requests
- **Error Handling:** The scraper includes fallback mechanisms, but some content may be unavailable
- **CSS Selectors:** Xiaohongshu's HTML structure may change, requiring selector updates

## 🐛 Troubleshooting

### "xhs_cookies.json not found"
- Make sure you've created the cookies file in the root directory
- Check the file format matches `xhs_cookies.json.example`

### "API Key not found"
- Verify your `.env` file exists and contains the correct API key
- Check that `LLM_PROVIDER` is set to either "openai" or "gemini"

### Scraping fails or returns "Content unavailable"
- Your cookies may have expired - export fresh cookies
- Xiaohongshu's HTML structure may have changed
- Check your internet connection

### Playwright errors
- Run `playwright install` to ensure browsers are installed
- On Linux, you may need additional system dependencies

## 📝 License

This project is for educational purposes. Please respect Xiaohongshu's Terms of Service when using this tool.

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!
