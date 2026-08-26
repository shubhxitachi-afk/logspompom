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

@app.on_message(filters.new_chat_members)
async def add_user_with_button(client, message):
    for user in message.new_chat_members:
        # User ka naam aur ID nikalna
        name = user.first_name
        user_id = user.id
        username = f"@{user.username}" if user.username else "None"
        
        # Message text format
        text = (
            f"👤 **New User Joined!**\n"
            f"┣ 👤 Name: {name}\n"
            f"┣ 🌐 Username: {username}\n"
            f"┗ 🆔 ID: `{user_id}`"
        )
        
        # Message ke niche direct profile khulne ke liye button
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Message User", url=f"tg://openmessage?user_id={user_id}")]
            ]
        )
        
        # Purana message delete karne ki koshish (Agar bot admin hoga tabhi chalega)
        try:
            await message.delete()
        except Exception as e:
            print(f"Could not delete message: {e}")
            
        # Naya custom formatted message button ke sath bhejna
        await client.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboard
        )

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
