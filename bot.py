import os
import asyncio
from pyrogram import Client, filters, idle

# ─── சூழல் மாறிகளிலிருந்து மதிப்புகளைப் பெறுதல் ───
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ─── சரிபார்ப்பு ───
if not (0 < API_ID <= 2147483647):
    raise ValueError(
        f"API_ID தவறானது: {API_ID}. "
        "my.telegram.org-இலிருந்து சரியான 7-8 இலக்க எண்ணைப் பெறவும்."
    )
if not API_HASH or len(API_HASH) != 32:
    raise ValueError(f"API_HASH தவறானது: {API_HASH!r}")
if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise ValueError(f"BOT_TOKEN தவறானது: {BOT_TOKEN[:20]!r}...")

print("=" * 50)
print(f"API_ID   = {API_ID}")
print(f"API_HASH = {API_HASH[:8]}...")
print(f"BOT_TOKEN= {BOT_TOKEN[:20]}...")
print("=" * 50)

# ─── Pyrogram Client ───
app = Client(
    "terabox_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "வணக்கம் நண்பா! 👋 நான் ஒரு Terabox Downloader Bot. "
        "உன்னோட Terabox லிங்க்க இங்கே அனுப்பு, நான் டவுன்லோட் பண்ணித் தர்றேன்!"
    )


@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def handle_terabox(client, message):
    text = message.text or ""
    if "terabox" in text.lower():
        await message.reply_text(
            "📥 உன்னோட Terabox லிங்க் கிடைச்சிருச்சு! "
            "வீடியோவை ப்ராசஸ் பண்ணிட்டு இருக்கேன்..."
        )
    else:
        await message.reply_text(
            "தயவுசெய்து ஒரு சரியான Terabox லிங்க்காக அனுப்புங்க நண்பா!"
        )


async def main():
    print("Bot is starting...")
    await app.start()
    print("Bot is running successfully!")
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
