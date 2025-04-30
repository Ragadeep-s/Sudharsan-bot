import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define projects
PROJECTS = {
    "Short Films": [
        {"name": "Echo", "image": "echo.jpg", "link": "https://youtube.com/shortfilm1"}
    ],
    "Webseries": [
        {"name": "Parallel Lives", "image": "parallel.jpg", "link": "https://youtube.com/webseries1"}
    ],
    "Pilot Films": [
        {"name": "Genesis", "image": "genesis.jpg", "link": "https://youtube.com/pilot1"}
    ],
    "Album Song": [
        {"name": "Dreamscape", "image": "dreamscape.jpg", "link": "https://youtube.com/song1"}
    ]
}

ABOUT_DIRECTOR_TEXT = """**Sudharsan Sedhuramne** is an independent filmmaker known for visually rich and emotionally resonant storytelling.
His works span across genres with a distinctive cinematic style.
"""

WHATSAPP_LINK = "https://wa.me/919999999999"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(name, callback_data=name)] for name in PROJECTS.keys()]
    buttons.append([InlineKeyboardButton("About Director", callback_data="about_director")])
    await update.message.reply_text("Welcome! Choose an option below:", reply_markup=InlineKeyboardMarkup(buttons))

# Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in PROJECTS:
        buttons = [[InlineKeyboardButton(p["name"], callback_data=f"project_{query.data}_{i}")]
                   for i, p in enumerate(PROJECTS[query.data])]
        await query.edit_message_text(f"Select a project from {query.data}:", reply_markup=InlineKeyboardMarkup(buttons))
    elif query.data.startswith("project_"):
        _, category, index = query.data.split("_", 2)
        project = PROJECTS[category][int(index)]
        image_path = f"images/{project['image']}"
        with open(image_path, 'rb') as img:
            await query.message.reply_photo(photo=img, caption=project["name"],
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton("Open Video", url=project["link"])]
                                            ]))
    elif query.data == "about_director":
        await query.edit_message_text(ABOUT_DIRECTOR_TEXT, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("Contact Director", url=WHATSAPP_LINK)]
                                      ]))

# Main app
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
