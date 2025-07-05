import os
import json
import time
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 22689107
API_HASH = "0b2dda9c11cf2d6bd85f1416a8d1f190"
BOT_TOKEN = "7380116829:AAEu-jSMWWaijeUNUxXKe2huz93itJl-N94"

YOUTUBE_LINK = "https://youtube.com/@ssc_cgl_helper?si=EuaHEG65AuFDw_qL"
TELEGRAM_CHANNEL = "https://t.me/+IhQPhZfuJLs2ODRl"

USERDATA_FILE = "userdata.json"
os.makedirs("screenshots", exist_ok=True)

user_step = {}
users_data = {}

# Load previous data if exists
if os.path.exists(USERDATA_FILE):
    with open(USERDATA_FILE, "r") as f:
        users_data = json.load(f)

app = Client("ssc_helper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = str(message.from_user.id)
    user_step[user_id] = "awaiting_name"
    message.reply_text(
        "👋 **Welcome to SSC CGL Helper Bot!**\n\n"
        "🎯 *Let's get started with your registration...*\n"
        "📝 Please send your **Full Name** to continue:"
    )

@app.on_message(filters.text & ~filters.command("start"))
def handle_text(client, message):
    user_id = str(message.from_user.id)
    text = message.text.strip()

    if user_id not in user_step:
        return message.reply_text("⚠️ Please type /start to begin.")

    step = user_step[user_id]

    if step == "awaiting_name":
        users_data[user_id] = {"name": text}
        user_step[user_id] = "awaiting_contact"
        message.reply_text(
            "📱 Now send your **Telegram Number** or **Username**:\n"
            "Example:\n`9876543210` or `@yourusername`"
        )

    elif step == "awaiting_contact":
        users_data[user_id]["contact"] = text
        user_step[user_id] = "awaiting_screenshot"

        with open(USERDATA_FILE, "w") as f:
            json.dump(users_data, f, indent=2)

        message.reply_text(
            "📢 **Please Subscribe to Our YouTube Channel**\n"
            f"🔗 {YOUTUBE_LINK}\n\n"
            "📸 *After subscribing, take a screenshot and send here.*\n"
            "⚠️ Make sure the screenshot clearly shows that you're subscribed.\n"
            "⏳ Waiting for your screenshot..."
        )

@app.on_message(filters.photo)
def handle_photo(client, message: Message):
    user_id = str(message.from_user.id)

    if user_id not in users_data:
        return message.reply_text("⚠️ Please register first by typing /start")

    user_info = users_data[user_id]
    name = user_info.get("name", "noname").replace(" ", "_")
    contact = user_info.get("contact", "nocontact").replace("@", "").replace(" ", "_")
    timestamp = int(time.time())

    filename = f"{name}_{contact}_{timestamp}.jpg"
    file_path = f"screenshots/{filename}"
    message.download(file_path)

    os.system(f"rclone copy \"{file_path}\" gdrive:subscribe_screenshots")

    message.reply_text(
        "✅ *Screenshot received and verified!*\n\n"
        "🎁 You’ve successfully completed the steps.\n\n"
        "📚 Join our Premium Telegram Channel:\n"
        f"🔗 {TELEGRAM_CHANNEL}\n\n"
        "🚀 *Best of luck for your preparation!* 💪"
    )

app.run()
