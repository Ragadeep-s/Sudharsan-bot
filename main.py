import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

PROJECTS = {
    "Short Films": [
        {"name": "Aalaporan Thamizhan", "image": "aalaporan.jpg", "link": "https://youtu.be/XKZR-be9dOo?si=00_mm6vnE9nSsJ9o"},
        {"name": "Kanave Kalaiyaathe", "image": "kanave.jpg", "link": "https://youtu.be/w9LEWldaFnQ?si=GUwhZ--HLvRWd7tY"},
        {"name": "Muthal Maatram Un Kaiyil", "image": "maatram.jpg", "link": "https://youtu.be/SXaz0GE7roM?si=Ca8Mpi3uc10nW5BF"},
        {"name": "Unnakkaga Vaazha Ninaikiren", "image": "unnakkaga.jpg", "link": "https://drive.google.com/file/d/1PgRkjzl9mdalfegW7PbrbeLqoBPvnfh2/view?usp=drivesdk"},
        {"name": "Scared", "image": "scared.jpg", "link": "https://drive.google.com/file/d/1ZLss10-kVZDSLbLfZ-bR4IaOsUuB7h1v/view?usp=drivesdk"}
    ],
    "Pilot Films": [
        {"name": "Mudintha Kathai Thodarvathillai", "image": "mudintha.jpg", "link": "https://youtu.be/W5V4A6Hjh18?si=FHp8k2OceaVj39z4"},
        {"name": "The Last Wish", "image": "lastwish.jpg", "link": "https://youtu.be/6qtU1gNlci4?si=axJy7dUHhD8eozEM"}
    ],
    "Webseries": [
        {"name": "Venpani Malare - Episode 1", "image": "venpani1.jpg", "link": "https://youtu.be/-rZWOW8UfIk?si=ilnmaO4l3HqP87RL"},
        {"name": "Venpani Malare - Episode 2", "image": "venpani2.jpg", "link": "https://youtu.be/CExeXTpKAe8?si=03E7xLIkBufeswfx"},
        {"name": "Venpani Malare - Episode 3", "image": "venpani3.jpg", "link": "https://youtu.be/UAaRp1lLx64?si=ptNRRngV7KfafG7G"},
        {"name": "Venpani Malare - Episode 4", "image": "venpani4.jpg", "link": "https://youtu.be/u2UAJkNf1Ao?si=Al3V0qvtyocYogEn"},
        {"name": "Venpani Malare - Episode 5", "image": "venpani5.jpg", "link": "https://youtu.be/TmORlTyNN-E?si=GPhwlBYFyKHfy4w"}
    ],
    "Album Song": [
        {"name": "Aval Peyar Dhatchaeni", "image": "dhatchaeni.jpg", "link": "https://youtu.be/zsN6838vfo4?si=fASfFevrAijeqZov"},
        {"name": "Avalo Athirai", "image": "athirai.jpg", "link": "https://youtu.be/aScKBJbHPdg?si=2meyCYMFrtubeBEa"}
    ]
}

ABOUT_DIRECTOR_TEXT = """🎥 **Sudharsan Sedhuramne** is an independent filmmaker whose work merges striking visuals and heartfelt storytelling. From **award-winning short films** and **captivating web series** to bold **pilot films** and immersive **album songs**, his creations redefine independent cinema. Every project reflects his innovative vision, crafting experiences that linger long after the screen fades.
"""
WHATSAPP_LINK = "https://wa.me/917092197506"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(name, callback_data=name)] for name in PROJECTS.keys()]
    buttons.append([InlineKeyboardButton("About Director", callback_data="about_director")])
    await update.message.reply_text("Welcome! Choose an option below:", reply_markup=InlineKeyboardMarkup(buttons))

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

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
