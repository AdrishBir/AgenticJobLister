from telegram_bot import run_telegram_bot
from logging_config import setup_logging

def main():
    """
    Main entry point of the application.
    Sets up logging and starts the Telegram bot.
    """
    setup_logging()
    run_telegram_bot()

if __name__ == "__main__":
    main()
