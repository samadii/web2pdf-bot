import os, re
from pyppeteer.errors import PageError, NetworkError, TimeoutError
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

Bot = Client(
    "Web2PDF-Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}, I am web2pdf Bot.

> `I can download webpages as PDF.`

Send any URL to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/samadii/web2pdf-bot'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.text)
async def webtopdf(_, m):
    url = m.text
    name = re.sub(r'^\w+://', '', url.lower())
    name = name.replace('/', '-') + '.pdf'
    msg = await m.reply("Processing..")
    try:
        pyppdf.save_pdf(name, url)
    except PageError:
        return await msg.edit('URL could not be resolved.')
    except TimeoutError:
        return await msg.edit('Timeout.')
    except NetworkError:
        return await msg.edit('No access to the network.')
    await m.reply_document(name)
    await msg.delete()
    os.remove(name)



Bot.run()
