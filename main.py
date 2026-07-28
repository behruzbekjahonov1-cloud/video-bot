import telebot
import yt_dlp
import os

TOKEN = os.getenv("7711970155:AAEIiCJB-cFWQ1tIOQwHRXzQkTdc9smV4ts")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 Salom!\n\n📥 Instagram, TikTok, YouTube, Facebook va boshqa video havolasini yuboring."
    )


@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text.strip()

    if not url.startswith(("http://", "https://")):
        bot.reply_to(message, "❌ Iltimos, video havolasini yuboring.")
        return

    status = bot.reply_to(message, "⏳ Video yuklanmoqda...")

    ydl_opts = {
        "format": "best",
        "outtmpl": "%(id)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video)

        os.remove(filename)
        bot.delete_message(message.chat.id, status.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Xatolik:\n{e}",
            message.chat.id,
            status.message_id,
        )


print("✅ Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)
