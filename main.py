import os
import sys
import requests
import threading
import asyncio
import logging

# Set up logging so Render catches all errors instantly
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FIX FOR NEWER PYTHON VERSIONS ---
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# -------------------------------------

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Fetch environment variables and strip accidental blank spaces
API_ID = os.environ.get("API_ID", "").strip()
API_HASH = os.environ.get("API_HASH", "").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
PORT = os.environ.get("PORT", "5000")

# Pre-flight check for missing credentials
if not API_ID or not API_HASH or not BOT_TOKEN:
    logger.error("❌ CRITICAL: Missing Environment Variables! Check API_ID, API_HASH, and BOT_TOKEN in Render Settings.")
    sys.exit(1)

try:
    api_id_int = int(API_ID)
except ValueError:
    logger.error(f"❌ CRITICAL: API_ID must be a number! You entered: '{API_ID}'")
    sys.exit(1)

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    return "TeraBox Bot is running online!"

def run_flask():
    try:
        app.run(host="0.0.0.0", port=int(PORT))
    except Exception as e:
        logger.error(f"Flask web server error: {e}")

# Initialize Telegram Bot Client
try:
    bot = Client(
        "terabox_bot",
        api_id=api_id_int,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
except Exception as e:
    logger.error(f"❌ Failed to initialize Telegram Client: {e}")
    sys.exit(1)

@bot.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text(
        "👋 Hello! I am a TeraBox Downloader Bot.\n\n"
        "🔗 Send me any TeraBox link, and I will extract the direct download video link for you."
    )

@bot.on_message(filters.text & filters.regex(r"(terabox\.com|teraboxapp\.com|teraboxlink\.com|1024tera\.com|nephobox\.com|4funbox\.com)"))
async def process_terabox(client, message: Message):
    terabox_url = message.text.strip()
    status_msg = await message.reply_text("⏳ Extracting direct link... Please wait.")
    
    try:
        api_url = f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={terabox_url}"
        response = requests.get(api_url).json()
        
        if response.get("response") and len(response["response"]) > 0:
            video_data = response["response"][0]
            resolutions = video_data.get("resolutions", {})
            direct_link = resolutions.get("Fast Download") or list(resolutions.values())[0]
            title = response.get("title", "Terabox Video")
            
            if direct_link:
                reply_text = (
                    f"📥 **Link Generated Successfully!**\n\n"
                    f"🎬 **Title:** `{title}`\n\n"
                    f"🔗 [Click Here to Download Video]({direct_link})\n\n"
                    f"_Note: Click the link to stream or download via your browser._"
                )
                await status_msg.edit_text(reply_text, disable_web_page_preview=True)
            else:
                await status_msg.edit_text("❌ Failed to extract the direct download link.")
        else:
            await status_msg.edit_text("❌ Invalid link or the Terabox API failed to bypass this URL.")
            
    except Exception as e:
        await status_msg.edit_text(f"⚠️ An error occurred: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting background web server...")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    logger.info("🤖 Bot is starting...")
    try:
        bot.run()
    except Exception as e:
        logger.error(f"❌ Bot crashed during runtime: {e}")
