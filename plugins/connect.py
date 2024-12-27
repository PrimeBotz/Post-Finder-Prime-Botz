from info import *
from utils import *
from client import User 
from pyrogram import Client, filters

@Client.on_message(filters.group & filters.command("connect"))
async def connect(bot, message):
    m=await message.reply("connecting..")
    user = await User.get_me()
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       channels  = group["channels"].copy()
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} can use this command 😁")
    if bool(verified)==False:
       return await m.edit("This chat is not verified!\nuse /verify")    
    try:
       channel = int(message.command[-1])
       if channel in channels:
          return await message.reply("This channel is already connected! You Cant Connect Again")
       channels.append(channel)
    except:
       return await m.edit("❌ Incorrect format!\nUse `/connect ChannelID`")    
    try:
       chat   = await bot.get_chat(channel)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link
       await User.join_chat(c_link)
    except Exception as e:
       if "The user is already a participant" in str(e):
          pass
       else:
          text = f"❌ Error: `{str(e)}`\nMake sure I'm admin in that channel & this group with all permissions and <a href='https://t.me/Prime_Nayem'>ᴍʀ.ᴘʀɪᴍᴇ</a> is not banned there"
          return await m.edit(text)
    await update_group(message.chat.id, {"channels":channels})
    await m.edit(f"✅ Successfully connected to [{chat.title}]({c_link})!\n\n একটা কথা বলি মনোযোগ দিয়ে শুনেন এডমিন ,\n অনেক সময় হঠাৎ করে একটু সমস্যা হয় যখন দেখবেন কোন কাজ করছে না বা কোন সমস্যা করছে বা রেস্পন্স করছে না তখন [{chat.title}]({c_link}) 👈 এখানে গিয়ে একবার /Start দিবেন তাহলে সুন্দর করে কাজ করবে আবার ধন্যবাদ\n\nLet me tell you something, listen carefully, admin,\n sometimes there is a sudden problem when you see that something is not working or having a problem or not responding. [{chat.title}]({c_link}) 👈 Go here and hit /Start once, it will work fine, thanks again.", disable_web_page_preview=True)
    text = f"#NewConnection\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("disconnect"))
async def disconnect(bot, message):
    m=await message.reply("Please wait..")   
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       channels  = group["channels"].copy()
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} can use this command 😁")
    if bool(verified)==False:
       return await m.edit("This chat is not verified!\nuse /verify")    
    try:
       channel = int(message.command[-1])
       if channel not in channels:
          return await m.edit("You didn't added this channel yet Or Check Channel Id")
       channels.remove(channel)
    except:
       return await m.edit("❌ Incorrect format!\nUse `/disconnect ChannelID`")
    try:
       chat   = await bot.get_chat(channel)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link
       await User.leave_chat(channel)
    except Exception as e:
       text = f"❌ Error: `{str(e)}`\nMake sure I'm admin in that channel & this group with all permissions and <a href='https://t.me/Prime_Nayem'>ᴍʀ.ᴘʀɪᴍᴇ</a> is not banned there"
       return await m.edit(text)
    await update_group(message.chat.id, {"channels":channels})
    await m.edit(f"✅ Successfully disconnected from [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#DisConnection\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("reset_grp"))
async def reset_grp(bot, message):
    m = await message.reply("Resetting group settings...")
    try:
        group = await get_group(message.chat.id)
        user_id = group["user_id"]
        user_name = group["user_name"]
        verified = group["verified"]
    except:
        return await bot.leave_chat(message.chat.id)
    
    if message.from_user.id != user_id:
        return await m.edit(f"Only {user_name} can use this command 😁")
    
    if not bool(verified):
        return await m.edit("This chat is not verified!\nUse /verify to verify this group.")
    
    try:
        # Reset group data
        default_data = {
            "channels": [],
            "f_sub": None,
        }
        await update_group(message.chat.id, default_data)
        await m.edit("✅ Group settings have been successfully reset!")
        
        # Log the reset
        group_info = await bot.get_chat(message.chat.id)
        group_link = group_info.invite_link
        log_text = (
            f"#GroupReset\n\nUser: {message.from_user.mention}\n"
            f"Group: [{group_info.title}]({group_link})\n"
            "Group settings have been reset to default."
        )
        await bot.send_message(chat_id=LOG_CHANNEL, text=log_text)
    except Exception as e:
        await m.edit(f"❌ Error: `{e}`")

@Client.on_message(filters.group & filters.command("connections"))
async def connections(bot, message):
    group     = await get_group(message.chat.id)    
    user_id   = group["user_id"]
    user_name = group["user_name"]
    channels  = group["channels"]
    f_sub     = group["f_sub"]
    if message.from_user.id!=user_id:
       return await message.reply(f"Only {user_name} can use this command 😁")
    if bool(channels)==False:
       return await message.reply("This group is currently not connected to any channels!\nConnect one using /connect")
    text = "This Group is currently connected to:\n\n"
    for channel in channels:
        try:
           chat = await bot.get_chat(channel)
           name = chat.title
           link = chat.invite_link
           text += f"🔗Connected Channel - [{name}]({link})\n"
        except Exception as e:
           await message.reply(f"❌ Error in `{channel}:`\n`{e}`")
    if bool(f_sub):
       try:
          f_chat  = await bot.get_chat(channel)
          f_title = f_chat.title
          f_link  = f_chat.invite_link
          text += f"\nFSub: [{f_title}]({f_link})"
       except Exception as e:
          await message.reply(f"❌ Error in FSub (`{f_sub}`)\n`{e}`")
   
    await message.reply(text=text, disable_web_page_preview=True)
  
