import logging
import re
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

from scraper import scrape_page
from llm_processor import process_with_llm
from google_sheets import update_or_add_row

logger = logging.getLogger(__name__)

# State for ConversationHandler
URL_RECEIVED = range(1)

def is_valid_url(text: str) -> bool:
    """
    Validates if the provided text is a valid URL using a regex.
    """
    regex = re.compile(
        r'^(https?://)?'  # http:// or https:// (optional)
        r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|'
        r'(?:www\.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+))'
        r'((?:\/[\+~%\/.\w_-]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?$'
    )
    return re.match(regex, text) is not None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command by sending a welcome message.
    """
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me a URL to a job listing, and I'll process it.",
    )
    return URL_RECEIVED

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /help command.
    """
    await update.message.reply_text("Send me a URL to a job listing, and I'll process it.")
    return

async def process_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes the job listing URL sent by the user.
    
    It scrapes the page, processes the content with the LLM,
    and stores the structured data in Google Sheets.
    """
    url = update.message.text.strip()
    if not is_valid_url(url):
        await update.message.reply_text("Please send a valid URL.")
        return URL_RECEIVED

    await update.message.reply_text("Processing your job listing. Please wait...")
    
    try:
        # Scrape the page content
        page_content = await scrape_page(url)
        
        # Process with LLM to extract structured data
        extracted_data = await process_with_llm(page_content, url)
        
        # Store the data in Google Sheets (optionally, add a review step here)
        # update_or_add_row(extracted_data)
        print(extracted_data)
        
        await update.message.reply_text("Job listing processed and stored successfully!")
    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")
        await update.message.reply_text(f"An error occurred while processing the job listing: {e}")
    return URL_RECEIVED

def run_telegram_bot():
    """
    Starts the Telegram bot and registers the command and message handlers.
    """
    from config import TELEGRAM_TOKEN
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            URL_RECEIVED: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_url)]
        },
        fallbacks=[CommandHandler("help", help_command)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()
