import os
import asyncio
from pyrogram import Client, filters, idle

# கோயப் / ரெண்டர்ல இருந்து Environment Variables-ஆ எடுக்கப் போறோம்
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# பாட்ட ஸ்டார்ட் பண்றோம்
app = Client(
    "terabox_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("வணக்கம் நண்பா! 👋 நான் ஒரு Terabox Downloader Bot. உன்னோட Terabox லிங்க்க இங்கே அனுப்பு, நான் டவுன்லோட் பண்ணித் தர்றேன்!")

@app.on_message(filters.text & filters.private)
async def handle_terabox(client, message):
    text = message.text
    if "terabox" in text.lower():
        await message.reply_text("📥 உன்னோட Terabox லிங்க் கிடைச்சிருச்சு! வீடியோவை ப்ராசஸ் பண்ணிட்டு இருக்கேன்...")
    else:
        await message.reply_text("தயவுசெய்து ஒரு சரியான Terabox லிங்க்காக அனுப்புங்க நண்பா!")

async def main():
    print("Bot is starting...")
    await app.start()
    print("Bot is running successfully!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
