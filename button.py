from pyrogram.types import InlineKeyboardButton
from enum import Enum

# Button ke styles define karne ke liye Enum
class ButtonStyle(Enum):
    SUCCESS = "success"
    PRIMARY = "primary"
    DANGER = "danger"

def styled_button(text: str, callback_data: str = None, url: str = None, user_id: int = None, style: ButtonStyle = ButtonStyle.PRIMARY):
    """
    Yeh ek custom wrapper hai Pyrogram ke InlineKeyboardButton ke liye.
    Isse aapka code clean rehta hai aur buttons systematically organize hote hain.
    """
    
    # Agar URL diya hai toh URL wala button banega
    if url:
        return InlineKeyboardButton(text=text, url=url)
        
    # Agar user_id di hai toh User mention wala button banega
    elif user_id:
        return InlineKeyboardButton(text=text, user_id=user_id)
        
    # Agar callback_data diya hai toh standard callback button banega (Sabse zyada use hone wala)
    elif callback_data:
        return InlineKeyboardButton(text=text, callback_data=callback_data)
        
    # Fallback agar galti se kuch pass nahi kiya gaya
    else:
        return InlineKeyboardButton(text=text, callback_data="none")
