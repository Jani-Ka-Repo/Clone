import random
from pyrogram import filters, Client
from pyrogram.types import Message

import config
from OraMusic import app
from OraMusic.core.call import Lucky
from OraMusic.misc import db

from OraMusic.utils.database import get_loop
from OraMusic.cplugin.utils.decorators.admins import AdminRightsCheck
from OraMusic.utils.inline import close_markup
from OraMusic.utils.stream.autoclear import auto_clean
from config import BANNED_USERS

@Client.on_message(
    filters.command(["skip", "cskip", "next", "cnext"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    # Queue check karte hain
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
        
    # Loop on/off check karte hain
    loop = await get_loop(chat_id)
    if loop != 0:
        return await message.reply_text(_["admin_8"])

    # Multi-skip logic (e.g., /skip 3)
    if len(message.command) > 1:
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            count = len(check)
            if count > 2:
                count = int(count - 1)
                if 1 <= state <= count:
                    for x in range(state - 1): # (state-1) times pop karenge
                        try:
                            popped = check.pop(0)
                            if popped:
                                await auto_clean(popped)
                        except:
                            pass
                else:
                    return await message.reply_text(_["admin_11"].format(count))
            else:
                return await message.reply_text(_["admin_10"])
        else:
            return await message.reply_text(_["admin_11"].format(len(check)-1))

    # 🟢 THE FIX: Delegate Everything to change_stream 🟢
    try:
        # Sahi PyTgCalls client (assistant) nikalte hain clone ke liye
        pytgcalls_client = Lucky.one
        if chat_id in Lucky.active_clients:
            val = Lucky.active_clients[chat_id]
            if isinstance(val, list) and len(val) > 0:
                pytgcalls_client = val[0]
            elif val and not isinstance(val, list):
                pytgcalls_client = val
                
        # Seedha change_stream call karo. 
        # Yeh khud current track pop karega, next play karega, aur UI stream_card bhej dega!
        await Lucky.change_stream(pytgcalls_client, chat_id)
        
    except Exception as e:
        # Agar error aaya toh music stop karke bot bahar aa jayega gracefully
        try:
            await message.reply_text(
                text=_["admin_6"].format(message.from_user.mention, message.chat.title),
                reply_markup=close_markup(_)
            )
            await Lucky.stop_stream(chat_id)
        except:
            pass
