# Don't Remove Credit Tg - https://t.me/Prime_Botz
# Subscribe Telegram Channel For Amazing Bot https://t.me/Prime_Botz
# Support Group Tg ➠ https://t.me/Prime_Botz_Support
# Ask Doubt on HTTPS://T.ME/MR_PRIME_SUPREME

import asyncio
from info import *
from utils import *
from time import time
from client import User
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# মেসেজ ডিলিট করার জন্য ফাংশন
async def delete_after_delay(message: Message, delay):
    await asyncio.sleep(delay)  
    try:
        await message.delete()  
    except:
        pass

# মেসেজ চাঙ্ক আকারে পাঠানোর জন্য ফাংশন
async def send_message_in_chunks(client, chat_id, text):
    max_length = 4096  # মেসেজের সর্বোচ্চ দৈর্ঘ্য
    for i in range(0, len(text), max_length):
        msg = await client.send_message(chat_id=chat_id, text=text[i:i+max_length])
        asyncio.create_task(delete_after_delay(msg, 300))  

# সার্চ মেসেজ হ্যান্ডলিং
@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub == False:
        return     
    channels = (await get_group(message.chat.id))["channels"]
    if bool(channels) == False:
        return     
    if message.text.startswith("/"):
        return    
    query = message.text  # সার্চ কুইয়েরি নিচ্ছে
    head = "<u>Here is the results 👇\n\n💢 Powered By </u> <b><I> @Prime_Botz ❗\n⋆★⋆━━━━━━★━━━━⋆★⋆\n</I></b>\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0]
                if name in results:
                    continue 
                results += f"<b><I>♻️𝗙𝗶𝗹𝗲 𝗡𝗮𝗺𝗲 : {name}\n\n🔗𝗟𝗶𝗻𝗸 ➠ {msg.link}</I></b>\n\n⋆★⋆━━━━━━★━━━━⋆★⋆\n\n"
        if bool(results) == False:  # যদি কোনো রেজাল্ট না মিলে
            movies = await search_imdb(query)
            buttons = []
            for movie in movies: 
                buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])
            msg = await message.reply_photo(
                photo="https://envs.sh/zTd.jpg",
                caption="<b><I>I Couldn't find anything related to Your Query😕.\nDid you mean any of these?</I></b>", 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            asyncio.create_task(delete_after_delay(message, 300))  
            asyncio.create_task(delete_after_delay(msg, 300))
        else:
            reply_message = await send_message_in_chunks(bot, message.chat.id, head + results)
            asyncio.create_task(delete_after_delay(message, 300))  
    except:
        pass

# ইমডিবি রি-চেক
@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:      
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete()       
    if clicked != typed:
        return await update.answer("That's not for you! 👀", show_alert=True)

    m = await update.message.edit("Prime Advance Ai Try To Searching..💥")
    id = update.data.split("_")[-1]
    query = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    head = "<u>I Have Searched Movie With Wrong Spelling But Take care next time 👇\n\n💢 Powered By </u> <b><I>@Prime_Botz ❗\n⋆★⋆━━━━━━★━━━━⋆★⋆</I></b>\n\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0]
                if name in results:
                    continue 
                results += f"<b><I>♻️𝗙𝗶𝗹𝗲 𝗡𝗮𝗺𝗲 🍿: {name}</I></b>\n\n🔗𝗟𝗶𝗻𝗸 ➠ {msg.link}</I></b>\n\n⋆★⋆━━━━━━★━━━━⋆★⋆\n\n"
        if bool(results) == False:          
            return await update.message.edit("Still no results found! Please Request To Group Admin", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Request To Admin 🎯", callback_data=f"request_{id}")]]))
        await update.message.edit(text=head + results, disable_web_page_preview=True)
        asyncio.create_task(delete_after_delay(update.message, 300))
    except Exception as e:
        await update.message.edit(f"❌ Error: `{e}`")

# এডমিনকে রিকোয়েস্ট
@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:      
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete()       
    if clicked != typed:
        return await update.answer("That's not for you! 👀", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    id = update.data.split("_")[1]
    name = await search_imdb(id)
    url = "https://www.imdb.com/title/tt" + id
    text = f"#RequestFromYourGroup\n\nName: {name}\nIMDb: {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("✅ Request Sent To Admin", show_alert=True)
    await update.message.delete()

# Don't Remove Credit Tg - https://t.me/Prime_Botz
# Subscribe Telegram Channel For Amazing Bot https://t.me/Prime_Botz
# Support Group Tg ➠ https://t.me/Prime_Botz_Support
# Ask Doubt on HTTPS://T.ME/MR_PRIME_SUPREME

    
