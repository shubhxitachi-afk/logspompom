import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
        user_id = match.group(1)
        
        # Callback button jo click hone par instant action lega
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Message User", callback_data=f"contact_{user_id}")]
            ]
        )
        
        try:
            await message.edit_text(
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Could not edit message: {e}")

# Jaise hi button par tap karoge, yeh function run hoga
@app.on_callback_query(filters.regex(r"^contact_"))
async def handle_contact_button(client, callback_query: CallbackQuery):
    user_id = callback_query.data.split("_")[1]
    
    # Ye user ko direct Telegram chat link popup mein dega
    profile_link = f"tg://user?id={user_id}"
    web_link = f"https://t.me/{user_id}" # Alternative fallback
    
    try:
        # Click karne wale ko alert mein direct link aur status dikhayega
        await callback_query.answer(
            f"User ID: {user_id}\nClick below or check bot PM for direct chat.",
            show_alert=True
        )
        
        # Bot aapko private (PM) mein clickable link bhej dega taaki aap turant msg bhej sako
        await client.send_message(
            chat_id=callback_query.from_user.id,
            text=f"👤 **Target User Contact Link**\n\n🆔 ID: `{user_id}`\n🔗 Direct Link: [Click Here to Message](tg://user?id={user_id})"
        )
    except Exception as e:
        # Agar bot se PM pehle shuru nahi hai toh group mein bhej dega
        await client.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"👤 User ID: `{user_id}`\n🔗 Chat Link: [Open Chat](tg://user?id={user_id})"
        )

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
