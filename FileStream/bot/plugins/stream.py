import asyncio
from FileStream.bot import FileStream, multi_clients
from FileStream.utils.bot_utils import is_user_banned, is_user_exist, is_user_joined, gen_link, is_channel_banned, is_channel_exist, is_user_authorized
from FileStream.utils.database import Database
from FileStream.utils.file_properties import get_file_ids, get_file_info
from FileStream.config import Telegram, Server
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode
import logging

# Initialize the database
db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_user_preference(user_id):
    # Placeholder function to get user preference from the database
    # Replace with actual logic to fetch user preference
    return True

async def get_hash(message):
    # Placeholder function to generate a hash for the message
    # Replace with actual logic
    return "dummy_hash"

async def get_name(message):
    # Placeholder function to get the file name
    # Replace with actual logic
    return "dummy_file_name"

async def humanbytes(size):
    # Placeholder function to convert size to human-readable format
    # Replace with actual logic
    return f"{size} bytes"

@FileStream.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.animation
        | filters.photo
    ),
    group=4,
)
async def private_receive_handler(bot: Client, message: Message):
    if not await is_user_authorized(message):
        return
    if await is_user_banned(message):
        return

    await is_user_exist(bot, message)
    if Telegram.FORCE_SUB:
        if not await is_user_joined(bot, message):
            return
    try:
        inserted_id = await db.add_file(get_file_info(message))
        await get_file_ids(False, inserted_id, multi_clients, message)
        reply_markup, stream_text = await gen_link(_id=inserted_id)
        
        user_preference = await get_user_preference(message.from_user.id)

        if user_preference:
            media = message.document or message.video or message.audio or message.photo or message.animation or message.voice or message.video_note
            if media:
                await bot.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=media.file_id,
                    caption=stream_text,
                    parse_mode=ParseMode.HTML
                )
        else:
            await message.reply_text(
                text=stream_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=reply_markup,
                quote=True
            )
    except FloodWait as e:
        logger.warning(f"Sleeping for {e.value}s due to FloodWait")
        await asyncio.sleep(e.value)
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {e.value}s ғʀᴏᴍ [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n**ᴜsᴇʀ ɪᴅ :** `{message.from_user.id}`",
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=f"**#EʀʀᴏʀTʀᴀᴄᴋᴇʙᴀᴄᴋ:** `{e}`",
            disable_web_page_preview=True
        )

@FileStream.on_message(
    filters.channel
    & ~filters.forwarded
    & ~filters.media_group
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.photo
    )
)
async def channel_receive_handler(bot: Client, msg: Message):
    if await is_channel_banned(bot, msg):
        return
    await is_channel_exist(bot, msg)

    try:
        file_caption = msg.caption if msg.caption else ""
        
        log_msg = await msg.forward(chat_id=Telegram.FLOG_CHANNEL)
        online_link = f"{Server.URL}dl/{str(log_msg.id)}?hash={await get_hash(log_msg)}"
        settings = await db.get_channel_detail(msg.chat.id)
        
        await log_msg.reply_text(
            text=f"**Channel Name:** `{msg.chat.title}`\n**CHANNEL ID:** `{msg.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {online_link}", 
            quote=True
        )
        
        await bot.edit_message_caption(
                    chat_id=msg.chat.id,
                    message_id=msg.id,
                    caption=settings['settings']["caption"].format(file_name ='' if get_name(log_msg) is None else get_name(log_msg),
                                             caption ='' if file_caption is None else file_caption, 
                                             download_link ='' if online_link is None else online_link, 
                                             stream_link ='' if online_link is None else online_link, 
                                            ),
                )
        
        await bot.edit_message_caption(
            chat_id=msg.chat.id,
            message_id=msg.id,
            caption=format(
                file_name='' if await get_name(log_msg) is None else await get_name(log_msg),
                caption='' if file_caption is None else file_caption, 
                file_size='' if await humanbytes(msg.document.file_size) is None else await humanbytes(msg.document.file_size),
                download_link='' if online_link is None else online_link, 
                stream_link='' if online_link is None else online_link
            ),
        )
    except FloodWait as w:
        logger.warning(f"Sleeping for {w.x}s due to FloodWait")
        await asyncio.sleep(w.x)
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=f"GOT FLOODWAIT OF {w.x}s FROM {msg.chat.title}\n\n**CHANNEL ID:** `{msg.chat.id}`",
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await bot.send_message(
            chat_id=Telegram.ULOG_CHANNEL,
            text=f"**#ERROR_TRACKEBACK:** `{e}`",
            disable_web_page_preview=True
        )
        logger.error(f"Can't edit broadcast message! Error: {e}")
