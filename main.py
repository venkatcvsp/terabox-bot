import os
import requests
import threading
import asyncio

# --- FIX FOR NEWER PYTHON VERSIONS ---
# Create an event loop before importing Pyrogram to prevent the RuntimeError
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# -------------------------------------

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Fetch environment variables from Render
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = os.environ.get("PORT", "5000")

# ... (keep the rest of your code exactly the same below this)
