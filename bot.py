import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

ADMINS = {6187018016}  # এখানে নিজের Telegram ID বসাও

users = set()
blocked_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    if user.id in blocked_users:
        return

    await update.message.reply_text(
        f"👋 Hello {user.first_name}\n\n"
        "🤖 Support Bot Active\n"
        "📩 /contact - Send message to admin\n"
        "❓ /help - Show commands"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 Available Commands:\n\n"
        "/start - Start bot\n"
        "/contact - Contact admin\n"
        "/help - Show help\n"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = True
    await update.message.reply_text("✍️ Write your message for admin:")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    if not context.user_data.get("contact"):
        return

    for admin in ADMINS:
        await context.bot.send_message(
            admin,
            f"📩 New Message\n\n"
            f"Name: {user.first_name}\n"
            f"ID: {user.id}\n\n"
            f"{update.message.text}"
        )

    await update.message.reply_text("✅ Message sent to admin")
    context.user_data["contact"] = False

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    await update.message.reply_text(
        f"👑 Admin Panel\n\n"
        f"Total Users: {len(users)}\n\n"
        "/broadcast <msg>\n"
        "/block <id>\n"
        "/unblock <id>"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    msg = " ".join(context.args)
    sent = 0

    for u in users:
        if u not in blocked_users:
            try:
                await context.bot.send_message(u, msg)
                sent += 1
            except:
                pass

    await update.message.reply_text(f"✅ Broadcast sent to {sent} users")

async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    blocked_users.add(int(context.args[0]))
    await update.message.reply_text("🚫 User blocked")

async def unblock_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return

    blocked_users.discard(int(context.args[0]))
    await update.message.reply_text("✅ User unblocked")

def main():
    print("🤖 Bot started successfully")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("block", block_user))
    app.add_handler(CommandHandler("unblock", unblock_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
