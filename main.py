from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os, logging

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

PROJECTS = {
    "Short Films": [
        {"name": "Aalaporan Thamizhan", "image": "aalaporan.jpg", "link": "https://youtu.be/XKZR-be9dOo?si=00_mm6vnE9nSsJ9o"},
        {"name": "Kanave Kalaiyaathe", "image": "kanave.jpg", "link": "https://youtu.be/w9LEWldaFnQ?si=GUwhZ--HLvRWd7tY"},
        {"name": "Muthal Maatram Un Kaiyil", "image": "maatram.jpg", "link": "https://youtu.be/SXaz0GE7roM?si=Ca8Mpi3uc10nW5BF"},
        {"name": "Unnakkaga Vaazha Ninaikiren", "image": "unnakkaga.jpg", "link": "https://drive.google.com/file/d/1PgRkjzl9mdalfegW7PbrbeLqoBPvnfh2/view?usp=drivesdk"},
        {"name": "Scared", "link": "https://drive.google.com/file/d/1ZLss10-kVZDSLbLfZ-bR4IaOsUuB7h1v/view?usp=drivesdk"}
    ],
    "Pilot Films": [
        {"name": "Mudintha Kathai Thodarvathillai", "image": "mudintha.jpg", "link": "https://youtu.be/W5V4A6Hjh18?si=FHp8k2OceaVj39z4"},
        {"name": "The Last Wish", "image": "lastwish.jpg", "link": "https://youtu.be/6qtU1gNlci4?si=axJy7dUHhD8eozEM"}
    ],
    "Webseries": [
        {"name": "Venpani Malare - Episode 1", "image": "venpani.jpg", "link": "https://youtu.be/-rZWOW8UfIk?si=ilnmaO4l3HqP87RL"},
        {"name": "Venpani Malare - Episode 2", "image": "venpani.jpg", "link": "https://youtu.be/CExeXTpKAe8?si=03E7xLIkBufeswfx"},
        {"name": "Venpani Malare - Episode 3", "image": "venpani.jpg", "link": "https://youtu.be/UAaRp1lLx64?si=ptNRRngV7KfafG7G"},
        {"name": "Venpani Malare - Episode 4", "image": "venpani.jpg", "link": "https://youtu.be/u2UAJkNf1Ao?si=Al3V0qvtyocYogEn"},
        {"name": "Venpani Malare - Episode 5", "image": "venpani.jpg", "link": "https://youtu.be/TmORlTyNN-E?si=GPhwlBYFyKHfy4w"}
    ],
    "Album Song": [
        {"name": "Aval Peyar Dhatchaeni", "image": "dhatchaeni.jpg", "link": "https://youtu.be/zsN6838vfo4?si=fASfFevrAijeqZov"},
        {"name": "Avalo Athirai", "image": "athirai.jpg", "link": "https://youtu.be/aScKBJbHPdg?si=2meyCYMFrtubeBEa"}
    ]
}

ABOUT_DIRECTOR_TEXT = (
    "\U0001F464 *Hi, I'm Sudharsan Sedouramane*\n\n"
    "A passionate \U0001F4DD storyteller, writer, and creative soul who believes in the power of \U0001F499 *words and emotions*.")
ABOUT_DIRECTOR_TEXT += (
    "\n\n\U0001F3A5 From journalism to \U0001F3AC filmmaking, I'm a *National Award winner* chasing meaningful content that resonates."
    "\n\n\U0001F339 *Avalo Athirai* is not just a project â€” it's a piece of my heart."
    "\n\nWhen Iâ€™m not writing, I enjoy deep conversations, clever humor, and the subtle beauty in everyday life."
    "\n\n\U0001F4F1 *Explore, connect, and join me on this creative journey.*"
)

WHATSAPP_LINK = "https://wa.me/917092197506"
INSTAGRAM_LINK = "https://www.instagram.com/sudharsan_sedouramane_official?igsh=azdtdXd0MGZrcjk1"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = "images/director_main.jpg"
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            await update.message.reply_photo(photo=img, caption="\U0001F3AC Director Sudharsan Sedhuramne\nCrafting stories beyond boundaries.")

    buttons = [[InlineKeyboardButton(name, callback_data=name)] for name in PROJECTS.keys()]
    buttons.append([InlineKeyboardButton("\U0001F464 About Director", callback_data="about_director")])
    await update.message.reply_text("\U0001F4FA *Welcome! View my projects below:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in PROJECTS:
        buttons = [[InlineKeyboardButton(p["name"], callback_data=f"project_{query.data}_{i}")]
                   for i, p in enumerate(PROJECTS[query.data])]
        buttons.append([InlineKeyboardButton("\u2B05 Back", callback_data="main_menu")])
        await query.edit_message_text(f"\U0001F4D6 *Select a project from {query.data}:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data.startswith("project_"):
        _, category, index = query.data.split("_", 2)
        project = PROJECTS[category][int(index)]
        image_path = f"images/{project.get('image', '')}"
        caption = f"\U0001F3AC *{project['name']}*"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("\U0001F517 Open Video", url=project["link"])],
            [InlineKeyboardButton("\u2B05 Back", callback_data=category)]
        ])

        if os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                await query.message.reply_photo(photo=img, caption=caption, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await query.message.reply_text(caption, parse_mode="Markdown", reply_markup=reply_markup)

    elif query.data == "about_director":
        about_image_path = "images/director_about.jpg"
        if os.path.exists(about_image_path):
            with open(about_image_path, 'rb') as img:
                await query.message.reply_photo(photo=img)

        await query.message.reply_text(ABOUT_DIRECTOR_TEXT, parse_mode="Markdown",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton("\U0001F4DE Contact Director", callback_data="contact_director")],
                                           [InlineKeyboardButton("\u2B05 Back", callback_data="main_menu")]
                                       ]))

    elif query.data == "contact_director":
        await query.message.reply_text("\U0001F4E9 *Contact Sudharsan through:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("\U0001F4F2 WhatsApp", url=WHATSAPP_LINK)],
            [InlineKeyboardButton("\U0001F4F7 Instagram", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton("\u2B05 Back", callback_data="about_director")]
        ]))

    elif query.data == "main_menu":
        buttons = [[InlineKeyboardButton(name, callback_data=name)] for name in PROJECTS.keys()]
        buttons.append([InlineKeyboardButton("\U0001F464 About Director", callback_data="about_director")])
        await query.edit_message_text("\U0001F4FA *Welcome! View my projects below:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))


async def set_bot_commands(app):
    # Set default commands shown in the Telegram menu
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("about", "About the Director"),
        BotCommand("projects", "View Projects"),
    ])

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


ABOUT_DIRECTOR_HTML = '''
<b>About the Director</b>

<img src="images/director_main.jpg"/>

<b>ðŸŽ¬ Name:</b> <i>Sudharsan</i>
<b>ðŸ† Passion:</b> <i>Independent Short Film Maker</i>
<b>âœ¨ Vision:</b> <i>Inspire through storytelling & meaningful visuals</i>

<b>Follow us on:</b>
ðŸ”— <a href="https://www.instagram.com/">Instagram</a> |
ðŸ”— <a href="https://www.youtube.com/">YouTube</a> |
ðŸ”— <a href="https://t.me/">Telegram</a>
'''
