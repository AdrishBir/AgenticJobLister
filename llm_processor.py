import asyncio
import logging
import json
import aiohttp

from utils import async_retry
from prompt_engineering import get_extraction_prompt
from config import OPENROUTER_API_KEY, OPENROUTER_ENDPOINT
from cache import cache

logger = logging.getLogger(__name__)

@async_retry(max_retries=3, delay=2)
async def call_openrouter_api(prompt: str) -> dict:
    """
    Calls the OpenRouter (DeepSeek LLM) API with the given prompt and returns the parsed JSON response.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    payload = {
        "model": "deepseek/deepseek-r1:free",  # Using DeepSeek Coder model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.2
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_ENDPOINT, headers=headers, json=payload) as response:
            response_text = await response.text()
            if response.status != 200:
                logger.error(f"OpenRouter API error: {response.status} - {response_text}")
                raise Exception("LLM API call failed")
            try:
                result = json.loads(response_text)
                return result['choices'][0]['message']['content']  # Extract the actual response content
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Response parsing failed: {e}")
                raise

async def process_with_llm(page_content: str, url: str) -> dict:
    """
    Processes the scraped page content using the LLM API to extract structured data.
    Implements caching to avoid redundant API calls.
    """
    cache_key = f"llm:{url}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        logger.info("Using cached LLM result.")
        return cached_result

    prompt = get_extraction_prompt(page_content, url)
    
    try:
        result = await call_openrouter_api(prompt)
        if not isinstance(result, dict):
            raise ValueError("LLM output is not a valid JSON object")
        # Cache the result for future use
        await cache.set(cache_key, result)
        return result
    except Exception as e:
        logger.error(f"LLM processing failed: {e}")
        raise
