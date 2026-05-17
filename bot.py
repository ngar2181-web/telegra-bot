from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= SETTINGS =================

TOKEN = "8907973283:AAG_2FPr84WYR1JFKy8abqQcc-7b0LHNtUA"

SUPPORT_ID = "@ZenVPN_ir"

CHANNEL_LINK = "https://t.me/+GA5A2MMOUglmMzE0"

CARD_NAME = "محمدی ریاض"
CARD_NUMBER = "6037691790069355"

# ================= PRICE LIST =================

FAST_NET_PRICES = {
    "1 گیگ": "290 هزار تومان",
    "2 گیگ": "580 هزار تومان",
    "3 گیگ": "870 هزار تومان",
    "4 گیگ": "1,160,000 تومان",
    "5 گیگ": "1,450,000 تومان",
    "6 گیگ": "1,740,000 تومان",
    "7 گیگ": "2,030,000 تومان",
    "8 گیگ": "2,320,000 تومان",
    "9 گیگ": "2,610,000 تومان",
    "10 گیگ": "2,900,000 تومان"
}

CHAT_NET_PRICES = {
    "1 گیگ": "190 هزار تومان",
    "2 گیگ": "380 هزار تومان",
    "3 گیگ": "570 هزار تومان",
    "4 گیگ": "760 هزار تومان",
    "5 گیگ": "950 هزار تومان",
    "6 گیگ": "1,140,000 تومان",
    "7 گیگ": "1,330,000 تومان",
    "8 گیگ": "1,520,000 تومان",
    "9 گیگ": "1,710,000 تومان",
    "10 گیگ": "1,900,000 تومان"
}

# ================= MAIN MENU =================

def main_menu():

    keyboard = [
        ["🔥 نت ملی اینستاگرام + تلگرام + واتساپ"],
        ["💬 نت ملی چت و پیام‌رسان"],
        ["📢 کانال ما", "🛠 پشتیبانی"],
        ["💰 تعرفه ها"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
🔥 به فروشگاه VipNet خوش آمدید

📢 قبل از خرید وارد کانال شوید:
{CHANNEL_LINK}

🎁 داخل کانال:
• قیمت های جدید
• تخفیف ها
• کانفیگ رایگان

قرار داده می‌شود ✅

━━━━━━━━━━━━━━

🔐 فروش کانفیگ نت ملی

✅ سرعت بالا
✅ تحویل فوری
✅ پشتیبانی فعال

لطفاً یکی از گزینه‌ها را انتخاب کنید 👇
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )

# ================= MESSAGE HANDLER =================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # ================= FAST NET =================

    if text == "🔥 نت ملی اینستاگرام + تلگرام + واتساپ":

        keyboard = [[gig] for gig in FAST_NET_PRICES.keys()]
        keyboard.append(["🔙 برگشت"])

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        context.user_data["plan_type"] = "FAST"

        await update.message.reply_text(
            """
🔥 نت ملی پرسرعت VIP

✅ مناسب:
• اینستاگرام
• تلگرام
• واتساپ
• تیک‌تاک
• ایمو
• یوتیوب

⚡ سرعت بسیار بالا

لطفاً حجم موردنظر را انتخاب کنید 👇
""",
            reply_markup=reply_markup
        )

    # ================= CHAT NET =================

    elif text == "💬 نت ملی چت و پیام‌رسان":

        keyboard = [[gig] for gig in CHAT_NET_PRICES.keys()]
        keyboard.append(["🔙 برگشت"])

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        context.user_data["plan_type"] = "CHAT"

        await update.message.reply_text(
            """
💬 نت ملی چت

✅ مناسب:
• واتساپ
• تلگرام
• ایمو

⚡ مخصوص پیام‌رسان ها

لطفاً حجم موردنظر را انتخاب کنید 👇
""",
            reply_markup=reply_markup
        )

    # ================= SELECT FAST PLAN =================

    elif text in FAST_NET_PRICES:

        price = FAST_NET_PRICES[text]

        await update.message.reply_text(
            f"""
💳 اطلاعات پرداخت

📦 حجم انتخابی:
{text}

💰 مبلغ:
{price}

━━━━━━━━━━━━━━

👤 نام صاحب کارت:
{CARD_NAME}

💳 شماره کارت:
{CARD_NUMBER}

━━━━━━━━━━━━━━

⚠️ لطفاً مبلغ را واریز کنید
و رسید را به پشتیبانی ارسال نمایید.

🛠 پشتیبانی:
{SUPPORT_ID}
"""
        )

    # ================= SELECT CHAT PLAN =================

    elif text in CHAT_NET_PRICES:

        price = CHAT_NET_PRICES[text]

        await update.message.reply_text(
            f"""
💳 اطلاعات پرداخت

📦 حجم انتخابی:
{text}

💰 مبلغ:
{price}

━━━━━━━━━━━━━━

👤 نام صاحب کارت:
{CARD_NAME}

💳 شماره کارت:
{CARD_NUMBER}

━━━━━━━━━━━━━━

⚠️ لطفاً مبلغ را واریز کنید
و رسید را به پشتیبانی ارسال نمایید.

🛠 پشتیبانی:
{SUPPORT_ID}
"""
        )

    # ================= SUPPORT =================

    elif text == "🛠 پشتیبانی":

        await update.message.reply_text(
            f"""
🛠 پشتیبانی آنلاین

درصورت مشکل پیام بدهید ✅

{SUPPORT_ID}
"""
        )

    # ================= CHANNEL =================

    elif text == "📢 کانال ما":

        await update.message.reply_text(
            f"""
📢 کانال رسمی ما:

{CHANNEL_LINK}

🎁 کانفیگ رایگان و تخفیف هم قرار می‌گیرد.
"""
        )

    # ================= PRICES =================

    elif text == "💰 تعرفه ها":

        fast_prices = "\n".join(
            [f"{k} ➜ {v}" for k, v in FAST_NET_PRICES.items()]
        )

        chat_prices = "\n".join(
            [f"{k} ➜ {v}" for k, v in CHAT_NET_PRICES.items()]
        )

        await update.message.reply_text(
            f"""
🔥 تعرفه نت پرسرعت

{fast_prices}

━━━━━━━━━━━━━━

💬 تعرفه نت چت

{chat_prices}
"""
        )

    # ================= BACK =================

    elif text == "🔙 برگشت":

        await update.message.reply_text(
            "🔙 به منوی اصلی برگشتید.",
            reply_markup=main_menu()
        )

    # ================= INVALID =================

    else:

        await update.message.reply_text(
            "❌ لطفاً از دکمه‌های ربات استفاده کنید."
        )

# ================= RUN BOT =================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message
        )
    )

    print("BOT IS ONLINE ✅")

    app.run_polling()

if __name__ == "__main__":
    main()