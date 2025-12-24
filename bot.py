import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# পরিবেশ ভেরিয়েবল থেকে টোকেন নেওয়া হবে
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start কমান্ড দেওয়া হলে যা হবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 বট অনলাইন আছে!")

# মেইন ফাংশন যেখানে বট রান হবে
def main():
    # এখানে বট টোকেন দিয়ে অ্যাপ্লিকেশন তৈরি হবে
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # /start কমান্ড হ্যান্ডলার যোগ করা
    app.add_handler(CommandHandler("start", start))
    
    # বট রান হবে
    app.run_polling()

# স্ক্রিপ্ট রান করার এন্ট্রি পয়েন্ট
if __name__ == "__main__":
    main()
