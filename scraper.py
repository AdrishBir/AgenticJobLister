import asyncio
import random
import logging
import aiohttp
from bs4 import BeautifulSoup

from config import SCRAPER_USER_AGENTS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

async def fetch_page(url: str) -> str:
    """
    Asynchronously fetches the page content of the given URL using a rotated user agent.
    """
    headers = {
        "User-Agent": random.choice(SCRAPER_USER_AGENTS)
    }
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                text = await response.text()
                return text
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise

async def scrape_page(url: str) -> str:
    """
    Scrapes the full page content for job listing processing.
    
    For JavaScript-heavy pages, consider integrating Selenium.
    """
    html_content = await fetch_page(url)
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script and style tags
    for script in soup(["script", "style"]):
        script.decompose()
        
    text = soup.get_text(separator="\n")
    return text.strip()
