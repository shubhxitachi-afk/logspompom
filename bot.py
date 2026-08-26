import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Aapki credentials aur Bot Token
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
    
    # Message ke andar se User ID nikalna
    match = re.search(r"ID[:\s]*`?(\d+)`?", text, re.IGNORECASE)
    
    if match:
        user_id = int(match.group(1))
        
        # Yahan URL schema ko update kiya gaya hai taaki click karne par chat trigger ho
        # Telegram desktop/mobile ke liye 'tg://user?id=' sabse behtar kaam karta hai
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Message User", url=f"tg://user?id={user_id}")]
            ]
        )
        
        try:
            await message.edit_text(
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Could not edit message: {e}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
