import os
import requests
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Fetch environment variables from Render
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = os.environ.get("PORT", "5000")

# Flask setup: Required by Render to keep the web service alive
app = Flask(__name__)

@app.route('/')
def home():
    return "TeraBox Bot is running online!"

def run_flask():
    app.run(host="0.0.0.0", port=int(PORT))

# Initialize Telegram Bot Client
bot = Client(
    "terabox_bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text(
        "👋 Hello! I am a TeraBox Downloader Bot.\n\n"
        "🔗 Send me any TeraBox link, and I will extract the direct download video link for you."
    )

# Listen for messages containing Terabox domains
@bot.on_message(filters.text & filters.regex(r"(terabox\.com|teraboxapp\.com|teraboxlink\.com|1024tera\.com|nephobox\.com|4funbox\.com)"))
async def process_terabox(client, message: Message):
    terabox_url = message.text.strip()
    status_msg = await message.reply_text("⏳ Extracting direct link... Please wait.")
    
    try:
        # Using a public Terabox Bypass API
        # Note: If this specific free API stops working in the future, you can swap the URL with another active Terabox API.
        api_url = f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={terabox_url}"
        response = requests.get(api_url).json()
        
        if response.get("response") and len(response["response"]) > 0:
            video_data = response["response"][0]
            
            # Fetch the Fast Download link or fallback to the first available resolution
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
                await status_msg.edit_text("❌ Failed to extract the direct download link from the response.")
        else:
            await status_msg.edit_text("❌ Invalid link or the Terabox API failed to bypass this URL. Ensure the video is public.")
            
    except Exception as e:
        await status_msg.edit_text(f"⚠️ An error occurred: {str(e)}")

if __name__ == "__main__":
    # 1. Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # 2. Start the Pyrogram Telegram Bot
    print("🤖 Bot is starting...")
    bot.run()
