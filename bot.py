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

CARD_NAME = "محمدی رباض"
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

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🔥 نت ملی اینستاگرام + تلگرام"],
        ["💬 نت ملی چت و پیام‌رسان"],
        ["💰 تعرفه ها", "🛠 پشتیبانی"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = """
🔐 فروشگاه رسمی کانفیگ نت ملی

✅ سرعت بالا
✅ تحویل فوری
✅ پشتیبانی فعال

لطفاً یکی از گزینه‌ها را انتخاب کنید 👇
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# ================= MESSAGE HANDLER =================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # ================= FAST NET =================

    if text == "🔥 نت ملی اینستاگرام + تلگرام":

        plans = "\n".join(
            [f"{k} ➜ {v}" for k, v in FAST_NET_PRICES.items()]
        )

        keyboard = [
            ["💳 کارت به کارت"],
            ["🔙 برگشت"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        context.user_data["plan_type"] = "FAST"

        await update.message.reply_text(
            f"""
🔥 کانفیگ VIP NET

✅ مناسب:
اینستاگرام
تلگرام
تیک‌تاک
یوتیوب

🚀 سرعت بسیار بالا
✅ بدون نیاز به بروزرسانی

💰 تعرفه ها:

{plans}

برای پرداخت روی «کارت به کارت» بزنید 👇
""",
            reply_markup=reply_markup
        )

    # ================= CHAT NET =================

    elif text == "💬 نت ملی چت و پیام‌رسان":

        plans = "\n".join(
            [f"{k} ➜ {v}" for k, v in CHAT_NET_PRICES.items()]
        )

        keyboard = [
            ["💳 کارت به کارت"],
            ["🔙 برگشت"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        context.user_data["plan_type"] = "CHAT"

        await update.message.reply_text(
            f"""
💬 کانفیگ CHAT NET

✅ مناسب:
واتساپ
تلگرام
ایمو
روبیکا

⚠️ هر 12 ساعت نیاز به بروزرسانی دارد

💰 تعرفه ها:

{plans}

برای پرداخت روی «کارت به کارت» بزنید 👇
""",
            reply_markup=reply_markup
        )

    # ================= PAYMENT =================

    elif text == "💳 کارت به کارت":

        await update.message.reply_text(
            f"""
💳 اطلاعات پرداخت

👤 نام صاحب کارت:
{CARD_NAME}

💳 شماره کارت:
{CARD_NUMBER}

━━━━━━━━━━━━━━

⚠️ بعد از واریز رسید را به پشتیبانی ارسال کنید.

🛠 پشتیبانی:
{SUPPORT_ID}
"""
        )

    # ================= SUPPORT =================

    elif text == "🛠 پشتیبانی":

        await update.message.reply_text(
            f"""
🛠 پشتیبانی آنلاین

هر مشکلی داشتید پیام بدهید ✅

آیدی پشتیبانی:
{SUPPORT_ID}
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
🔥 تعرفه VIP NET

{fast_prices}

━━━━━━━━━━━━━━

💬 تعرفه CHAT NET

{chat_prices}
"""
        )

    # ================= BACK =================

    elif text == "🔙 برگشت":

        keyboard = [
            ["🔥 نت ملی اینستاگرام + تلگرام"],
            ["💬 نت ملی چت و پیام‌رسان"],
            ["💰 تعرفه ها", "🛠 پشتیبانی"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "🔙 به منوی اصلی برگشتید.",
            reply_markup=reply_markup
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