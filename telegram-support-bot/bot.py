import asyncio
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

load_dotenv()  # Load environment variables from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID  = int(os.getenv("ADMIN_ID"))   # convert to integer

# Optional: safety check
if not BOT_TOKEN or not ADMIN_ID:
    raise ValueError("BOT_TOKEN or ADMIN_ID not found in .env file")

message_map: dict[int, int] = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Adminဆီကိုဒီကနေစာပို့ထားလိုရပါတယ်။")

async def user_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == ADMIN_ID:
        return

    user_id = update.effective_chat.id
    forwarded = await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )
    if forwarded:
        message_map[forwarded.message_id] = user_id

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg.reply_to_message:
        await msg.reply_text("client ဆီ reply ပြန်ပါ။")
        return

    replied_id = msg.reply_to_message.message_id
    user_id = message_map.get(replied_id)

    if not user_id and msg.reply_to_message.forward_from:
        user_id = msg.reply_to_message.forward_from.id

    if not user_id:
        await msg.reply_text("Cannot identify client (hidden forward or old message)")
        return

    for attempt in range(1, 4):
        try:
            await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
            await msg.reply_text("Reply sent ✓")
            return
        except telegram.error.TimedOut:
            if attempt == 3:
                await msg.reply_text("Failed after 3 attempts (timeout)")
            else:
                await asyncio.sleep(2.5)
                continue
        except telegram.error.NetworkError as e:
            if attempt == 3:
                await msg.reply_text(f"Network error: {str(e)[:80]}")
            else:
                await asyncio.sleep(2.5)
                continue
        except Exception as e:
            await msg.reply_text(f"Error: {str(e)[:80]}")
            break

def main():
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .read_timeout(40.0)
        .write_timeout(40.0)
        .connect_timeout(15.0)
        .pool_timeout(40.0)
        .get_updates_read_timeout(60.0)   # helps with polling stability
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Chat(ADMIN_ID) & ~filters.COMMAND, admin_reply))
    application.add_handler(MessageHandler(~filters.Chat(ADMIN_ID) & ~filters.COMMAND, user_to_admin))

    print("Bot starting...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()