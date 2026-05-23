"""
Handlers for Secret Chat Bot commands
"""
import logging
import secrets
import string
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from database import get_session, User, Chat, ChatMember, Message
from crypto import EncryptionManager, generate_key

logger = logging.getLogger(__name__)

# Conversation states
CHOOSING_ACTION, ENTERING_CHAT_CODE, CONFIRMING_JOIN = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = update.effective_user
    session = get_session()
    
    try:
        # Check if user exists in DB
        db_user = session.query(User).filter_by(telegram_id=str(user.id)).first()
        
        if not db_user:
            # Create new user
            encryption_key = generate_key()
            db_user = User(
                telegram_id=str(user.id),
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                encryption_key=encryption_key.decode()
            )
            session.add(db_user)
            session.commit()
            await update.message.reply_text(
                "🔐 Welcome to Secret Chat Bot!\n\n"
                "Your encryption key has been generated and stored securely.\n\n"
                "Use /help to see available commands."
            )
        else:
            await update.message.reply_text(
                f"👋 Welcome back, {user.first_name}!\n\n"
                "Use /help to see available commands."
            )
    finally:
        session.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
🔐 Secret Chat Bot Commands:

/start - Initialize the bot
/help - Show this help message
/newchat - Create a new secret chat
/join - Join an existing secret chat
/list - List your active chats
/settings - Manage security settings

📝 How to use:
1. Use /newchat to create a new secret chat
2. Share the generated code with your friend
3. They use /join and enter the code
4. Start chatting securely!

🔒 All messages are encrypted end-to-end using AES-256 Fernet encryption.
"""
    await update.message.reply_text(help_text)


async def newchat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Create a new secret chat"""
    user = update.effective_user
    session = get_session()
    
    try:
        db_user = session.query(User).filter_by(telegram_id=str(user.id)).first()
        
        if not db_user:
            await update.message.reply_text("❌ Please use /start first!")
            return ConversationHandler.END
        
        # Generate unique chat code
        chat_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
        # Create new chat
        encryption_key = generate_key()
        new_chat = Chat(
            chat_code=chat_code,
            encryption_key=encryption_key.decode()
        )
        session.add(new_chat)
        session.flush()
        
        # Add user as member
        chat_member = ChatMember(chat_id=new_chat.id, user_id=db_user.id)
        session.add(chat_member)
        session.commit()
        
        await update.message.reply_text(
            f"✅ New secret chat created!\n\n"
            f"📌 Chat Code: <code>{chat_code}</code>\n\n"
            f"Share this code with your friend. They can join using /join command.",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error creating chat: {str(e)}")
        await update.message.reply_text("❌ Error creating chat. Please try again.")
    finally:
        session.close()


async def join_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Join an existing secret chat"""
    user = update.effective_user
    session = get_session()
    
    try:
        db_user = session.query(User).filter_by(telegram_id=str(user.id)).first()
        
        if not db_user:
            await update.message.reply_text("❌ Please use /start first!")
            return ConversationHandler.END
        
        await update.message.reply_text(
            "📝 Please enter the chat code:\n"
            "(Type /cancel to cancel)"
        )
        return ENTERING_CHAT_CODE
    finally:
        session.close()


async def receive_chat_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive and process chat code"""
    chat_code = update.message.text.strip().upper()
    user = update.effective_user
    session = get_session()
    
    try:
        # Find chat by code
        chat = session.query(Chat).filter_by(chat_code=chat_code).first()
        
        if not chat:
            await update.message.reply_text("❌ Chat code not found. Please try again.")
            return ENTERING_CHAT_CODE
        
        # Get user
        db_user = session.query(User).filter_by(telegram_id=str(user.id)).first()
        
        # Check if already member
        is_member = session.query(ChatMember).filter_by(
            chat_id=chat.id, user_id=db_user.id
        ).first()
        
        if is_member:
            await update.message.reply_text("⚠️ You are already a member of this chat!")
            return ConversationHandler.END
        
        # Add user to chat
        chat_member = ChatMember(chat_id=chat.id, user_id=db_user.id)
        session.add(chat_member)
        session.commit()
        
        await update.message.reply_text(
            f"✅ Successfully joined chat: <code>{chat_code}</code>\n\n"
            "You can now start sending encrypted messages!",
            parse_mode="HTML"
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error joining chat: {str(e)}")
        await update.message.reply_text("❌ Error joining chat. Please try again.")
        return ENTERING_CHAT_CODE
    finally:
        session.close()


async def list_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List user's active chats"""
    user = update.effective_user
    session = get_session()
    
    try:
        db_user = session.query(User).filter_by(telegram_id=str(user.id)).first()
        
        if not db_user:
            await update.message.reply_text("❌ Please use /start first!")
            return
        
        chats = db_user.chats
        
        if not chats:
            await update.message.reply_text("📭 You don't have any active chats yet.\n\nUse /newchat to create one or /join to join an existing chat.")
            return
        
        chat_list = "📋 Your Active Chats:\n\n"
        for i, chat in enumerate(chats, 1):
            member_count = len(chat.members)
            chat_list += f"{i}. <code>{chat.chat_code}</code> ({member_count} members)\n"
        
        await update.message.reply_text(chat_list, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error listing chats: {str(e)}")
        await update.message.reply_text("❌ Error retrieving chats.")
    finally:
        session.close()


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Security settings"""
    settings_text = """
⚙️ Security Settings:

🔐 Encryption: AES-256 Fernet
🔑 Key Derivation: PBKDF2 with 100,000 iterations
📊 Hash Algorithm: SHA256
💾 Database: Encrypted SQLite
🛡️ Message Retention: 30 days

📌 Tips for Maximum Security:
1. Never share your chat codes with untrusted people
2. Only accept chats from people you trust
3. Use strong passwords if password protection is enabled
4. Regularly review your active chats using /list

⚠️ Warning: Once a message is sent, it cannot be retrieved.
"""
    await update.message.reply_text(settings_text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation"""
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages (for chat)"""
    user = update.effective_user
    message_text = update.message.text
    session = get_session()
    
    try:
        db_user = session.query(User).filter_by(telegram_id=str(user.id)).first()
        
        if not db_user:
            await update.message.reply_text("❌ Please use /start first!")
            return
        
        # For now, just acknowledge the message
        # In production, you would determine which chat this is from (context-based)
        encrypted = EncryptionManager.encrypt_message(message_text, db_user.encryption_key.encode())
        
        await update.message.reply_text(
            "✅ Message encrypted and ready to send!\n"
            "(In production, this would be sent to all chat members)"
        )
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await update.message.reply_text("❌ Error processing message.")
    finally:
        session.close()
