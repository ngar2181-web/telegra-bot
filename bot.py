import os
import sqlite3
import logging
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8460547264

SUPPORT_ID = "@ZenVPN_ir"

CHANNEL_LINK = "https://t.me/+GA5A2MMOUglmMzE0"

CARD_NAME = "محمدی ریاض"

CARD_NUMBER = "6037691790069355"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# =========================
# DATABASE
# =========================


def get_db():
    conn = sqlite3.connect("orders.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


db = get_db()
cursor = db.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    plan_type TEXT,
    plan TEXT,
    price TEXT,
    status TEXT,
    created_at TEXT
)
"""
)

db.commit()

# =========================
# PRICES
# =========================

FAST_NET_PRICES = {
    "1": ("1 گیگ", "290 هزار تومان"),
    "2": ("2 گیگ", "580 هزار تومان"),
    "3": ("3 گیگ", "870 هزار تومان"),
    "5": ("5 گیگ", "1,450,000 تومان"),
    "10": ("10 گیگ", "2,900,000 تومان"),
}

# نت مخصوص اینستاگرام / تلگرام / تیک‌تاک

CHAT_NET_PRICES = {
    "1": ("1 گیگ", "187 هزار تومان"),
    "2": ("2 گیگ", "374 هزار تومان"),
    "3": ("3 گیگ", "561 هزار تومان"),
    "5": ("5 گیگ", "935 هزار تومان"),
    "10": ("10 گیگ", "1,870,000 تومان"),
}

# نت مخصوص چت واتساپ / تلگرام / ایمو

# =========================
# HELPERS
# =========================


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 نت ملی پرسرعت",
                callback_data="fast",
            )
        ],
        [
            InlineKeyboardButton(
                "💬 نت چت",
                callback_data="chat",
            )
        ],
        [
            InlineKeyboardButton(
                "📚 آموزش اتصال",
                callback_data="learn",
            )
        ],
        [
            InlineKeyboardButton(
                "📢 کانال",
                url=CHANNEL_LINK,
            )
        ],
        [
            InlineKeyboardButton(
                "🛠 پشتیبانی",
                url=f"https://t.me/{SUPPORT_ID.replace('@', '')}",
            )
        ],
        [
            InlineKeyboardButton(
                "💰 تعرفه‌ها",
                callback_data="prices",
            )
        ],

        [
            InlineKeyboardButton(
                "🎁 کانفیگ رایگان",
                url=CHANNEL_LINK,
            )
        ],

        [
            InlineKeyboardButton(
                "❓ اگر مشکل دارید",
                url=f"https://t.me/{SUPPORT_ID.replace('@', '')}",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def safe_edit(query, text, reply_markup=None):
    try:
        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
        )
    except Exception as e:
        logger.warning(f"Edit message failed: {e}")


# =========================
# START
# =========================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
🔥 به فروشگاه VipNet خوش آمدید

━━━━━━━━━━━━━━

⚡ فروش کانفیگ نت ملی

✅ سرعت بالا
✅ تحویل سریع
✅ پشتیبانی فعال

━━━━━━━━━━━━━━

📢 کانال:
{CHANNEL_LINK}

━━━━━━━━━━━━━━

لطفاً انتخاب کنید 👇
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu(),
    )


# =========================
# CALLBACKS
# =========================


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    data = query.data

    # =====================
    # FAST
    # =====================

    if data == "fast":
        keyboard = []

        for key, value in FAST_NET_PRICES.items():
            keyboard.append(
                [
                    InlineKeyboardButton(
                        value[0],
                        callback_data=f"buy|fast|{key}",
                    )
                ]
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back",
                )
            ]
        )

        await safe_edit(
            query,
            """
🔥 نت ملی پرسرعت

✅ اینستاگرام
✅ تلگرام
✅ واتساپ
✅ یوتیوب

حجم را انتخاب کنید 👇
""",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # =====================
    # CHAT
    # =====================

    elif data == "chat":
        keyboard = []

        for key, value in CHAT_NET_PRICES.items():
            keyboard.append(
                [
                    InlineKeyboardButton(
                        value[0],
                        callback_data=f"buy|chat|{key}",
                    )
                ]
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back",
                )
            ]
        )

        await safe_edit(
            query,
            """
💬 نت چت

✅ تلگرام
✅ واتساپ

⚠️ فقط پیام‌رسان

حجم را انتخاب کنید 👇
""",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # =====================
    # BUY
    # =====================

    elif data.startswith("buy|"):
        split_data = data.split("|")

        plan_type = split_data[1]
        plan_key = split_data[2]

        # جلوگیری از سفارش تکراری

        user_id = query.from_user.id

        cursor.execute(
            """
            SELECT * FROM orders
            WHERE user_id = ?
            AND status = 'PENDING'
            """,
            (user_id,),
        )

        existing = cursor.fetchone()

        if existing:
            await query.answer(
                "شما یک سفارش در انتظار دارید",
                show_alert=True,
            )
            return

        if plan_type == "fast":
            plan, price = FAST_NET_PRICES[plan_key]
            title = "🔥 نت پرسرعت"
        else:
            plan, price = CHAT_NET_PRICES[plan_key]
            title = "💬 نت چت"

        user = query.from_user

        username = user.username or "NoUsername"

        cursor.execute(
            """
            INSERT INTO orders (
                user_id,
                username,
                plan_type,
                plan,
                price,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.id,
                username,
                plan_type,
                plan,
                price,
                "PENDING",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        db.commit()

        order_id = cursor.lastrowid

        context.user_data["waiting_receipt"] = order_id

        await safe_edit(
            query,
            f"""
{title}

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

⚠️ لطفاً مبلغ را واریز کنید
و سپس عکس رسید را همینجا ارسال نمایید.

🧾 شماره سفارش:
#{order_id}
""",
        )

    # =====================
    # LEARN
    # =====================

    elif data == "learn":
        await safe_edit(
            query,
            f"""
📚 آموزش اتصال

برای دریافت آموزش:
{SUPPORT_ID}
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="back",
                        )
                    ]
                ]
            ),
        )

    # =====================
    # PRICES
    # =====================

    elif data == "prices":
        fast_prices = "\n".join(
            [f"{v[0]} ➜ {v[1]}" for v in FAST_NET_PRICES.values()]
        )

        chat_prices = "\n".join(
            [f"{v[0]} ➜ {v[1]}" for v in CHAT_NET_PRICES.values()]
        )

        await safe_edit(
            query,
            f"""
🔥 تعرفه نت پرسرعت

{fast_prices}

━━━━━━━━━━━━━━

💬 تعرفه نت چت

{chat_prices}
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت",
                            callback_data="back",
                        )
                    ]
                ]
            ),
        )

    # =====================
    # BACK
    # =====================

    elif data == "back":
        await safe_edit(
            query,
            "🏠 منوی اصلی",
            reply_markup=main_menu(),
        )

    # =====================
    # APPROVE
    # =====================

    elif data.startswith("approve_"):
        if query.from_user.id != ADMIN_ID:
            await query.answer(
                "دسترسی ندارید",
                show_alert=True,
            )
            return

        order_id = data.split("_")[1]

        cursor.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE id = ?
            """,
            ("APPROVED", order_id),
        )

        db.commit()

        cursor.execute(
            "SELECT user_id FROM orders WHERE id = ?",
            (order_id,),
        )

        row = cursor.fetchone()

        if not row:
            return

        user_id = row[0]

        await context.bot.send_message(
            chat_id=user_id,
            text="""
✅ پرداخت شما تایید شد

🛠 لطفاً جهت دریافت کانفیگ
به پشتیبانی پیام دهید:

@ZenVPN_ir
""",
        )

        caption = query.message.caption or ""

        await query.message.edit_caption(
            caption=caption + "\n\n✅ تایید شد"
        )

    # =====================
    # REJECT
    # =====================

    elif data.startswith("reject_"):
        if query.from_user.id != ADMIN_ID:
            await query.answer(
                "دسترسی ندارید",
                show_alert=True,
            )
            return

        order_id = data.split("_")[1]

        cursor.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE id = ?
            """,
            ("REJECTED", order_id),
        )

        db.commit()

        cursor.execute(
            "SELECT user_id FROM orders WHERE id = ?",
            (order_id,),
        )

        row = cursor.fetchone()

        if not row:
            return

        user_id = row[0]

        await context.bot.send_message(
            chat_id=user_id,
            text="""
❌ رسید شما تایید نشد

لطفاً مجدد بررسی و ارسال کنید.
""",
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
    context: ContextTypes.DEFAULT_TYPE,
):
    if "waiting_receipt" not in context.user_data:
        await update.message.reply_text(
            "❌ ابتدا یک پلن انتخاب کنید."
        )
        return

    order_id = context.user_data["waiting_receipt"]

    user = update.message.from_user

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ تایید",
                    callback_data=f"approve_{order_id}",
                ),
                InlineKeyboardButton(
                    "❌ رد",
                    callback_data=f"reject_{order_id}",
                ),
            ]
        ]
    )

    # عکس

    if update.message.photo:
        file_id = update.message.photo[-1].file_id

    # فایل عکس

    elif (
        update.message.document
        and update.message.document.mime_type
        and update.message.document.mime_type.startswith("image/")
    ):
        file_id = update.message.document.file_id

    else:
        await update.message.reply_text(
            "❌ لطفاً فقط تصویر رسید ارسال کنید"
        )
        return

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"""
🧾 رسید جدید

👤 کاربر:
{user.first_name}

🆔 آیدی:
{user.id}

📦 سفارش:
#{order_id}
""",
        reply_markup=keyboard,
    )

    await update.message.reply_text(
        """
✅ رسید دریافت شد

بعد از تایید ادمین،
وضعیت سفارش اعلام می‌شود.
"""
    )

    del context.user_data["waiting_receipt"]


# =========================
# FALLBACK MESSAGE
# =========================


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "برای شروع از /start استفاده کنید"
    )


# =========================
# ERROR HANDLER
# =========================


async def error_handler(update, context):
    logger.exception(context.error)


# =========================
# MAIN
# =========================


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(callbacks))

    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.IMAGE,
            receipt_handler,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    app.add_error_handler(error_handler)

    logger.info("BOT IS ONLINE ✅")

    app.run_polling()


# =========================
# RUN
# =========================


if __name__ == "__main__":
    try:
        main()
    finally:
        db.close()