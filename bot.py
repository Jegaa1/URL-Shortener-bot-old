import os
import aiohttp
from pyrogram import Client, filters

API_ID = 1923471
API_HASH = "fcdc178451cd234e63faefd38895c991"
BOT_TOKEN = "5477637816:AAFH5szsoiJPsEhOzW9S0ZfsEpXIKOhjvB0"
API_KEY = "003db0d0a2e56943b93dc0abd80e1260a17166c8"
WEBSITE = "tnlink.in"


try:
    bot = Client('shortener bot',
                 api_id=int(API_ID),
                 api_hash=API_HASH,
                 plugins = dict(root="plugins"),
                 bot_token=BOT_TOKEN,
                 workers=50,
                 sleep_threshold=10)
except Exception:
    print("Add var values properly. Read readme.md once")


@bot.on_message(filters.command('start'))
async def start(bot, message):
    start_msg = f"""
Hi {message.chat.first_name}!

I'm {WEBSITE} bot. Just send me link and get short link!

Send me a link to short a link with random alias.

For custom alias, <code>[link] | [custom_alias]</code>, Send in this format\n
Ex: https://t.me/example | Example

    """
    await message.reply_text(start_msg, disable_web_page_preview=True, quote=True)


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    if "|" in message.text:
        link_parts = message.text.split("|")
        link = link_parts[0]
        aliases = link_parts[1:len(message.text) + 1]
        alias1 = ""
        for alias in aliases:
            alias1 += alias
        x = alias1.replace(" ", "")
    else:
        link = message.matches[0].group(0)
        x= ""
    short_link = await get_shortlink(link, x)
    await message.reply(short_link, quote=True)


async def get_shortlink(link, x):
    url = f'https://{WEBSITE}/api'
    params = {'api': API_KEY,
              'url': link,
              'alias': x
              }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            print(data["status"])
            if data["status"] == "success":
                return f"<code>{data['shortenedUrl']}</code>\n\nLink:\n{data['shortenedUrl']}"
            else:
                return f"Error: {data['message']}"

bot.run()
