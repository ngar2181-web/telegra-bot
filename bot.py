import sqlite3
import logging
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

TOKEN = "YOUR_BOT_TOKEN"

ADMIN_ID = 8460547264

SUPPORT_ID = "@ZenVPN_ir"

CHANNEL_LINK = "https://t.me/ZenVPN_i"

CHANNEL_USERNAME = "@ZenVPN_i"

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
    "1 گیگ": "290 هزار تومان",
    "2 گیگ": "580 هزار تومان",
    "3 گیگ": "870 هزار تومان",
    "5 گیگ": "1,450,000 تومان",
    "10 گیگ": "2,900,000 تومان"
}

CHEAP_PRICES = {
    "1 گیگ": "190 هزار تومان",
    "2 گیگ": "380 هزار تومان",
    "3 گیگ": "570 هزار تومان",
    "5 گیگ": "950 هزار تومان",
    "10 گیگ": "1,900,000 تومان"
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
            "creator",
            "owner"
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
                "🔥 نت ملی اینستاگرام + تلگرام + واتساپ",
                callback_data="vip"
            )
        ],

        [
            InlineKeyboardButton(
                "💬 نت ملی چت و پیامرسان",
                callback_data="cheap"
            )
        ],

        [
            InlineKeyboardButton(
                "🎁 کانفیگ رایگان",
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
                "📢 کانال ما",
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
            "❌ ابتدا عضو کانال شوید",
            reply_markup=keyboard
        )

        return

    text = f"""
🔥 به فروشگاه رسمی ZenVPN خوش آمدید

━━━━━━━━━━━━━━

⚡ فروش انواع کانفیگ پرسرعت
⚡ تحویل سریع
⚡ پشتیبانی فعال

━━━━━━━━━━━━━━

🛠 پشتیبانی:
{SUPPORT_ID}

👇 یکی از گزینه‌ها را انتخاب کنید
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

        await context.bot.send_message(
            chat_id=user.id,
            text="✅ عضویت تایید شد\n\nدوباره /start را ارسال کنید"
        )

    # =====================
    # VIP
    # =====================

    elif data == "vip":

        keyboard = []

        for plan, price in VIP_PRICES.items():

            keyboard.append([
                InlineKeyboardButton(
                    f"{plan} | {price}",
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
🔥 نت ملی اینستاگرام

✅ مناسب:
• اینستاگرام
• تلگرام
• واتساپ
• یوتیوب

⚡ سرعت بالا

👇 حجم را انتخاب کنید
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================
    # CHEAP
    # =====================

    elif data == "cheap":

        keyboard = []

        for plan, price in CHEAP_PRICES.items():

            keyboard.append([
                InlineKeyboardButton(
                    f"{plan} | {price}",
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
💬 نت ملی چت

✅ مناسب:
• تلگرام
• واتساپ
• ایمو

⚠️ فقط مناسب چت

👇 حجم را انتخاب کنید
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================
    # BUY
    # =====================

    elif data.startswith("buy_"):

        _, plan_type, plan = data.split("_", 2)

        if plan_type == "vip":
            price = VIP_PRICES[plan]
            panel_name = "نت ملی اینستاگرام"
        else:
            price = CHEAP_PRICES[plan]
            panel_name = "نت ملی چت"

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
                f"{panel_name} - {plan}",
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
                    "🔙 بازگشت",
                    callback_data="back"
                )
            ]
        ])

        await query.message.edit_text(
            f"""
💳 اطلاعات پرداخت

━━━━━━━━━━━━━━

📦 سرویس:
{panel_name}

📦 حجم:
{plan}

💰 مبلغ:
{price}

━━━━━━━━━━━━━━

👤 نام صاحب کارت:
{CARD_NAME}

💳 شماره کارت:
{CARD_NUMBER}

━━━━━━━━━━━━━━

🧾 شماره سفارش:
#{order_id}

⚠️ مبلغ را واریز کنید
و سپس عکس رسید را ارسال نمایید.
""",
            reply_markup=keyboard
        )

    # =====================
    # SUPPORT
    # =====================

    elif data == "support":

        await query.message.edit_text(
            f"""
🛠 پشتیبانی

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
    # FREE
    # =====================

    elif data == "free":

        await query.message.edit_text(
            f"""
🎁 کانفیگ رایگان

1️⃣ عضو کانال شوید
2️⃣ به پشتیبانی پیام دهید

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
            "🏠 به منوی اصلی برگشتید",
            reply_markup=main_menu()
        )

    # =====================
    # APPROVE
    # =====================

    elif data.startswith("approve_"):

        if user.id != ADMIN_ID:
            return

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

        caption = query.message.caption or ""

        await query.message.edit_caption(
            caption=caption + "\n\n✅ تایید شد"
        )

    # =====================
    # REJECT
    # =====================

    elif data.startswith("reject_"):

        if user.id != ADMIN_ID:
            return

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
            "❌ رسید شما رد شد"
        )

        caption = query.message.caption or ""

        await query.message.edit_caption(
            caption=caption + "\n\n❌ رد شد"
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
            "❌ ابتدا سفارش ثبت کنید"
        )

        return

    order_id = context.user_data["receipt"]

    if not update.message.photo:

        await update.message.reply_text(
            "❌ لطفاً عکس رسید ارسال کنید"
        )

        return

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

    try:

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
✅ رسید شما ارسال شد

⏳ لطفاً منتظر تایید ادمین باشید
"""
        )

        del context.user_data["receipt"]

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "❌ خطا در ارسال رسید"
        )

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

    print("BOT ONLINE ✅")

    app.run_polling()

# =========================
# RUN
# =========================

if __name__ == "__main__":

    main()