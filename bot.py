import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_ID = 34829388
API_HASH = "30df7fd725bd39aa2e3b7a55b15a182b"
BOT_TOKEN = "8303039257:AAEvpXb-rDdQEu_OILt8d6Lxqq736p3Xn_U"

app = Client(
    "user_button_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.text & ~filters.me)
async def add_button_to_id_message(client, message):
    text = message.text
    
    # Message se User ID nikalna
    match = re.search(r"ID[:\s]*`?(\d+)`?", text, re.IGNORECASE)
    
    if match:
        user_id = match.group(1)
        
        # Callback button jo click hone par bot ko trigger karega
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Message User", callback_data=f"get_user_{user_id}")]
            ]
        )
        
        try:
            await message.edit_text(
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Could not edit message: {e}")

# Jab koi button par click karega
@app.on_callback_query(filters.regex(r"^get_user_"))
async def open_user_chat(client, callback_query: CallbackQuery):
    user_id = callback_query.data.split("_")[2]
    
    # User ko ek direct clickable mention/link ke sath message bhejenge
    # Telegram markdown me [Name](tg://user?id=...) sabse sahi kaam karta hai jab samne wale ki chat kholni ho
    response_text = (
        f"👤 **Target User Details:**\n"
        f"🆔 ID: `{user_id}`\n\n"
        f"👉 Click here to chat: [Open Private Chat](tg://user?id={user_id})"
    )
    
    try:
        # Click karne wale ke sath private chat me ya group me turant link bhej dega
        await callback_query.message.reply_text(response_text)
        await callback_query.answer("Link generated below! 👇", show_alert=False)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
