import os
import sys
import logging
import traceback
from threading import Thread

from flask import Flask
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
log = logging.getLogger(__name__)

# ---------- Config சரிபார்ப்பு ----------
def get_config():
    api_id_raw = os.environ.get("API_ID", "").strip()
    api_hash = os.environ.get("API_HASH", "").strip()
    bot_token = os.environ.get("BOT_TOKEN", "").strip()

    if not api_id_raw.isdigit():
        sys.exit(f"API_ID தவறு: எண்ணாக இல்லை (நீளம் {len(api_id_raw)})")
    if len(api_id_raw) > 10:
        sys.exit("API_ID மிகப் பெரியது: தவறான மதிப்பு போட்டிருக்கிறீர்கள்")
    if len(api_hash) != 32:
        sys.exit(f"API_HASH நீளம் 32 ஆக இருக்க வேண்டும், இப்போது {len(api_hash)}")
    if ":" not in bot_token:
        sys.exit("BOT_TOKEN தவறு: colon (:) இல்லை")

    return int(api_id_raw), api_hash, bot_token

API_ID, API_HASH, BOT_TOKEN = get_config()

# ---------- Flask keep-alive ----------
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# ---------- Pyrogram bot ----------
app = Client(
    "terabox_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,   # session file தேவையில்லை
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("வணக்கம்! Bot வேலை செய்கிறது ✅")

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    log.info("Bot is starting...")
    try:
        app.run()
    except Exception:
        log.error("Bot crashed:\n%s", traceback.format_exc())  # முழு traceback
        sys.exit(1)
