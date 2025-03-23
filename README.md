# AI Agentic Framework for Processing Job Listings

This project implements an AI agentic framework that integrates with a Telegram bot to process job listings. The system performs the following tasks:

1. **Receive a URL:** The Telegram bot receives a URL to a job listing.
2. **Web Scraping:** The system scrapes the page content using asynchronous HTTP requests and BeautifulSoup.
3. **LLM Processing:** The scraped content is processed using DeepSeek LLM via the OpenRouter API with a refined prompt.
4. **Google Sheets Storage:** The extracted structured data is stored in a Google Sheet.

## Features

- **Telegram Bot Integration:** Built using `python-telegram-bot` with asynchronous handlers.
- **Web Scraping Module:** Uses `aiohttp` and `BeautifulSoup` for robust content extraction with user-agent rotation.
- **LLM Processing Module:** Integrates with OpenRouter API, includes prompt engineering and smart retry logic.
- **Google Sheets Integration:** Utilizes the Google Sheets API to update or append job listing data.
- **Modular Design:** Each core component is implemented in its own module.
- **Caching:** Simple in-memory caching to avoid redundant LLM calls.
- **Logging & Error Handling:** Comprehensive logging, error handling, and retry mechanisms are in place.
- **Security:** API keys and sensitive data are managed via environment variables.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
