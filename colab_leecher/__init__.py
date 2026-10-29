# copyright 2023 © Xron Trix | https://github.com/cinelix

import logging, json
import asyncio # CHANGED
import uvloop # CHANGED
from pyrogram.client import Client

# Read the dictionary from the txt file
with open("/content/Telegram-Leecher/credentials.json", "r") as file:
    credentials = json.loads(file.read())

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]

logging.basicConfig(level=logging.INFO)

# --- FIX START ---
# Install uvloop policy
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Explicitly create and set a new loop so Pyrogram can find it
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# --- FIX END ---

colab_bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
