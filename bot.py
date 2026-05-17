import sqlite3
import logging
import os
import time
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# =========================
# CONFIG
# =========================

TOKEN = "8907973283:AAG_2FPr84WYR1JFKy8abqQcc-7b0LHNtUA"

ADMIN_ID = 8460547264

SUPPORT_ID = "@ZenVPN_ir"

CHANNEL_LINK = "https://t.me/+GA5A2MMOUglmMzE0"

CHANNEL_USERNAME = "@ZenVPN_ir"

CARD_NAME = "محمدی ریاض"

CARD_NUMBER = "6037691790069355"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(
    "orders.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        plan TEXT,
        price TEXT,
        status TEXT,
        created_at TEXT
    )
    """
)

conn.commit()

# =========================
# PRICES
# =========================

VIP_PRICES = {
    "1 گیگ": "284 هزار تومان",
    "2 گیگ": "568 هزار تومان",
    "3 گیگ": "852 هزار تومان",
    "5 گیگ": "1,420,000 تومان",
    "10 گیگ": "2,840,000 تومان"
}

CHEAP_PRICES = {
    "1 گیگ": "185 هزار تومان",
    "2 گیگ": "370 هزار تومان",
    "3 گیگ": "555 هزار تومان",
    "5 گیگ": "925 هزار تومان",
    "10 گیگ": "1,850,000 تومان"
}

# =========================
# SPAM PROTECTION
# =========================

spam_protection = {}


def anti_spam(user_id):

    now = time.time()

    if user_id in spam_protection:

        if now - spam_protection[user_id] < 2:
            return False

    spam_protection[user_id] = now

    return True

# =========================
# MEMBERSHIP CHECK
# =========================

async def check_member(bot, user_id):

    try:

        member = await bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:

        return False

# =========================
# MAIN MENU
# =========================


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🔥 خرید کانفیگ",
                callback_data="vip"
            )
        ],

        [
            InlineKeyboardButton(
                "💎 پنل اقتصادی",
                callback_data="cheap"
            )
        ],

        [
            InlineKeyboardButton(
                "🎁 دریافت کانفیگ رایگان",
                callback_data="free"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 قیمت همکاری",
                callback_data="co"
            )
        ],

        [
            InlineKeyboardButton(
                "🛠 پشتیبانی",
                callback_data="support"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 کانال رسمی",
                url=CHANNEL_LINK
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    member = await check_member(
        context.bot,
        user.id
    )

    if not member:

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 عضویت در کانال",
                    url=CHANNEL_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ عضو شدم",
                    callback_data="check_join"
                )
            ]
        ])

        await update.message.reply_text(
            """
❌ برای استفاده از ربات ابتدا عضو کانال شوید
""",
            reply_markup=keyboard
        )

        return

    text = f"""
🔥 به فروشگاه رسمی ZenVPN خوش آمدید

━━━━━━━━━━━━━━

⚡ اینترنت مخصوص شبکه‌های اجتماعی
⚡ سرعت بالا و پایدار
⚡ تحویل سریع
⚡ پشتیبانی فعال

━━━━━━━━━━━━━━

✅ مناسب اینستاگرام
✅ تلگرام
✅ واتساپ
✅ یوتیوب
✅ تیک‌تاک

━━━━━━━━━━━━━━

🛠 پشتیبانی:
{SUPPORT_ID}

لطفاً انتخاب کنید 👇
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )

# =========================
# CALLBACKS
# =========================

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    user = query.from_user

    if not anti_spam(user.id):

        await query.answer(
            "کمی صبر کنید",
            show_alert=True
        )

        return

    await query.answer()

    data = query.data

    # =====================
    # CHECK JOIN
    # =====================

    if data == "check_join":

        member = await check_member(
            context.bot,
            user.id
        )

        if not member:

            await query.answer(
                "هنوز عضو کانال نشدید",
                show_alert=True
            )

            return

        await query.message.delete()

        text = """
✅ عضویت تایید شد

دوباره /start را ارسال کنید
"""

        await context.bot.send_message(
            chat_id=user.id,
            text=text
        )

    # =====================
    # VIP PANEL
    # =====================

    elif data == "vip":

        keyboard = []

        for plan in VIP_PRICES:

            keyboard.append([
                InlineKeyboardButton(
                    f"{plan} ➜ {VIP_PRICES[plan]}",
                    callback_data=f"buy_vip_{plan}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back"
            )
        ])

        await query.message.edit_text(
            """
🔥 پنل VIP اجتماعی

✅ مناسب:
• اینستاگرام
• تلگرام
• واتساپ
• تیک‌تاک
• یوتیوب

⚡ سرعت بالا
⚡ پینگ مناسب
⚡ پایداری بهتر

📦 حجم موردنظر را انتخاب کنید 👇
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================
    # CHEAP PANEL
    # =====================

    elif data == "cheap":

        keyboard = []

        for plan in CHEAP_PRICES:

            keyboard.append([
                InlineKeyboardButton(
                    f"{plan} ➜ {CHEAP_PRICES[plan]}",
                    callback_data=f"buy_cheap_{plan}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back"
            )
        ])

        await query.message.edit_text(
            """
💎 پنل اقتصادی و چت

✅ مناسب:
• تلگرام
• واتساپ
• ایمو
• پیام‌رسان خارجی

⚠️ فقط مناسب چت
⚠️ ممکن است گاهی ناپایدار شود

📦 حجم موردنظر را انتخاب کنید 👇
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================
    # BUY
    # =====================

    elif data.startswith("buy_"):

        split_data = data.split("_")

        plan_type = split_data[1]

        plan = split_data[2]

        if plan_type == "vip":
            price = VIP_PRICES[plan]
        else:
            price = CHEAP_PRICES[plan]

        cursor.execute(
            """
            INSERT INTO orders (
                user_id,
                username,
                plan,
                price,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user.id,
                user.username,
                plan,
                price,
                "PENDING",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        conn.commit()

        order_id = cursor.lastrowid

        context.user_data["receipt"] = order_id

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "❌ لغو سفارش",
                    callback_data="back"
                )
            ]
        ])

        await query.message.edit_text(
            f"""
🧾 ثبت سفارش

━━━━━━━━━━━━━━

📦 حجم:
{plan}

💰 مبلغ:
{price}

━━━━━━━━━━━━━━

👤 صاحب کارت:
{CARD_NAME}

💳 شماره کارت:
{CARD_NUMBER}

━━━━━━━━━━━━━━

🧾 شماره سفارش:
#{order_id}

⚠️ لطفاً مبلغ را واریز کرده
و سپس عکس رسید را ارسال کنید.

✅ سفارش شما بعد از تایید پرداخت
در سریع‌ترین زمان بررسی می‌شود.
""",
            reply_markup=keyboard
        )

    # =====================
    # SUPPORT
    # =====================

    elif data == "support":

        await query.message.edit_text(
            f"""
🛠 پشتیبانی ZenVPN

درصورت وجود هرگونه مشکل:

{SUPPORT_ID}
""",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data="back"
                    )
                ]
            ])
        )

    # =====================
    # FREE CONFIG
    # =====================

    elif data == "free":

        await query.message.edit_text(
            f"""
🎁 دریافت کانفیگ رایگان

1️⃣ عضو کانال شوید
2️⃣ سپس به پشتیبانی پیام دهید

📢 کانال:
{CHANNEL_LINK}

🛠 پشتیبانی:
{SUPPORT_ID}
""",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data="back"
                    )
                ]
            ])
        )

    # =====================
    # COOPERATION
    # =====================

    elif data == "co":

        await query.message.edit_text(
            f"""
💰 قیمت همکاری

برای دریافت تعرفه همکاری:

{SUPPORT_ID}
""",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت",
                        callback_data="back"
                    )
                ]
            ])
        )

    # =====================
    # BACK
    # =====================

    elif data == "back":

        await query.message.edit_text(
            "🏠 منوی اصلی",
            reply_markup=main_menu()
        )

    # =====================
    # APPROVE
    # =====================

    elif data.startswith("approve_"):

        order_id = data.split("_")[1]

        cursor.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            ("APPROVED", order_id)
        )

        conn.commit()

        cursor.execute(
            "SELECT user_id FROM orders WHERE id = ?",
            (order_id,)
        )

        user_id = cursor.fetchone()[0]

        await context.bot.send_message(
            user_id,
            f"""
✅ پرداخت شما تایید شد

🛠 جهت دریافت کانفیگ:
{SUPPORT_ID}
"""
        )

        await query.message.edit_caption(
            caption=query.message.caption + "\n\n✅ تایید شد"
        )

    # =====================
    # REJECT
    # =====================

    elif data.startswith("reject_"):

        order_id = data.split("_")[1]

        cursor.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            ("REJECTED", order_id)
        )

        conn.commit()

        cursor.execute(
            "SELECT user_id FROM orders WHERE id = ?",
            (order_id,)
        )

        user_id = cursor.fetchone()[0]

        await context.bot.send_message(
            user_id,
            "❌ رسید تایید نشد"
        )

        await query.message.edit_caption(
            caption=query.message.caption + "\n\n❌ رد شد"
        )

# =========================
# RECEIPT HANDLER
# =========================

async def receipt_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if "receipt" not in context.user_data:

        await update.message.reply_text(
            "❌ ابتدا خرید انجام دهید"
        )

        return

    order_id = context.user_data["receipt"]

    photo = update.message.photo[-1]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ تایید",
                callback_data=f"approve_{order_id}"
            ),
            InlineKeyboardButton(
                "❌ رد",
                callback_data=f"reject_{order_id}"
            )
        ]
    ])

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=f"""
🧾 رسید جدید

👤 نام:
{user.first_name}

🆔 آیدی:
{user.id}

📦 سفارش:
#{order_id}
""",
        reply_markup=keyboard
    )

    await update.message.reply_text(
        """
✅ رسید دریافت شد

بعد از تایید ادمین
وضعیت سفارش اعلام می‌شود.
"""
    )

    del context.user_data["receipt"]

# =========================
# ERROR HANDLER
# =========================

async def error_handler(update, context):

    print(context.error)

# =========================
# MAIN
# =========================


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(callbacks)
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receipt_handler
        )
    )

    app.add_error_handler(error_handler)

    print("ZENVPN BOT ONLINE ✅")

    app.run_polling()

# =========================
# RUN
# =========================

if __name__ == "__main__":

    main()