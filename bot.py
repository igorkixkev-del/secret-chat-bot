"""
Secret Chat Bot for Telegram
Main application entry point
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

from config import TELEGRAM_BOT_TOKEN
from database import init_db
from handlers import (
    start, help_command, newchat, join_chat, receive_chat_code,
    list_chats, settings, cancel, handle_message,
    ENTERING_CHAT_CODE
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot"""
    # Initialize database
    init_db()
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_chats))
    application.add_handler(CommandHandler("settings", settings))
    
    # Add conversation handler for join_chat
    join_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("join", join_chat)],
        states={
            ENTERING_CHAT_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_chat_code)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(join_conv_handler)
    
    # Add newchat command handler
    application.add_handler(CommandHandler("newchat", newchat))
    
    # Add message handler for regular messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    logger.info("Starting Secret Chat Bot...")
    application.run_polling()


if __name__ == '__main__':
    main()
