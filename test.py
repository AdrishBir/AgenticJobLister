import os
import json
import logging
import asyncio
from openai import OpenAI
from prompt_engineering import get_extraction_prompt
from config import OPENROUTER_API_KEY, OPENROUTER_ENDPOINT
from cache import cache  # cache.get and cache.set are async

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure the OpenAI client to point to OpenRouter
client = OpenAI(
    base_url=OPENROUTER_ENDPOINT or "https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
)

class OpenRouterAPI:
    def __init__(self, model="deepseek/deepseek-r1:free", temperature=0.2, max_tokens=512):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = client

    def call_api(self, prompt: str) -> str:
        """
        Calls the OpenRouter API with the given prompt and returns the API response content.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            logger.debug("Raw API response: %s", response)
            result = response.choices[0].message.content
            return result
        except Exception as e:
            logger.error("OpenRouter API error: %s", e)
            raise Exception("LLM API call failed") from e

async def process_with_llm_async(page_content: str, url: str) -> dict:
    """
    Processes page content using the LLM API asynchronously.
    Uses caching to avoid redundant API calls.
    """
    cache_key = f"llm:{url}"
    # Directly await the asynchronous cache.get call.
    cached_result = await cache.get(cache_key)
    if cached_result:
        logger.info("Using cached LLM result.")
        return cached_result

    prompt = get_extraction_prompt(page_content, url)
    logger.debug("Generated prompt: %s", prompt)
    
    api = OpenRouterAPI()
    # Run the synchronous API call in a thread.
    result_str = await asyncio.to_thread(api.call_api, prompt)
    logger.debug("API result string: %s", result_str)
    
    try:
        result = json.loads(result_str)
        if result is None:
            logger.error("LLM output is empty (null).")
            raise Exception("LLM output is empty")
    except Exception as e:
        logger.error("Response parsing failed: %s", e)
        raise Exception("Failed to parse LLM output as JSON") from e

    # Directly await the asynchronous cache.set call.
    await cache.set(cache_key, result)
    return result

async def test_llm():
    test_url = "https://example.com/job"
    test_content = """
    Job Title: Senior Software Engineer
    Company: Example Corp
    Location: Remote
    
    We are looking for a Senior Software Engineer to join our team...
    """
    try:
        result = await process_with_llm_async(test_content, test_url)
        print("LLM extraction result:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm())
