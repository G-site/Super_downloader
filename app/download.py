from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from io import BytesIO
import asyncio
import tempfile
import os
import uuid
import re
import sqlite3
import yt_dlp

from app.database import download_user
from app.language import get_text
from main import bot

downloader = Router()
user_video_data = {}

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def check_lang(user_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT lang FROM users WHERE tg_id = ?", [user_id])
    lang = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return lang[0] if lang else "ru"

@downloader.message(
    lambda m: m.text.startswith("http") and any(x in m.text for x in ["watch?v=", "youtu.be/"])
)
async def handle_url(message: Message):
    lang = check_lang(message.from_user.id)
    url = message.text
    msg = await message.answer(get_text(lang, "search"))
    print("URL:", url)
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'extract_flat': False,
        'socket_timeout': 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info or info.get('_type') in ('playlist', 'channel', 'multi_video'):
                await msg.edit_text(get_text(lang, "incorect_link"))
                return

            title = info.get('title', '---')
            photo_url = info.get('thumbnail', None)

            formats = [
                f for f in info.get('formats', []) if f.get('ext') == 'mp4' and f.get('height')
            ]
            if not formats:
                await msg.edit_text(get_text(lang, "incorect_link"))
                return

            unique_formats = {}
            for f in formats:
                h = f['height']
                if h not in unique_formats or f.get('tbr', 0) > unique_formats[h].get('tbr', 0):
                    unique_formats[h] = f

            formats = sorted(unique_formats.values(), key=lambda x: x['height'], reverse=True)

            user_video_data[message.chat.id] = {
                "url": url,
                "formats": formats,
                "info": info
            }

            builder = InlineKeyboardBuilder()
            for fmt in formats[:6]:
                text = f"✅{fmt['height']}p"
                builder.button(text=text, callback_data=f"quality_{fmt['format_id']}")
            builder.button(text="🎵 MP3", callback_data="quality_mp3")
            builder.adjust(2)
            builder.row()

            await msg.delete()
            choose = get_text(lang, "choose")
            await message.answer_photo(
                photo=photo_url,
                caption=f"📽 <b>{title}</b>\n{choose}",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )

    except Exception as e:
        await msg.edit_text(get_text(lang, "incorect_link"))
        print(f'{e}')


@downloader.callback_query(F.data == "quality_mp3")
async def process_mp3(callback: CallbackQuery):
    lang = check_lang(callback.from_user.id)
    tg_id = callback.from_user.id
    chat_id = callback.message.chat.id

    await callback.answer(get_text(lang, "inicilization"))

    data = user_video_data.get(chat_id)
    if not data:
        await callback.message.edit_text(get_text(lang, "incorect_link"))
        return

    url = data["url"]
    title = data["info"].get("title", "audio_file")
    safe_title = sanitize_filename(title)

    await callback.message.delete()
    msg = await callback.message.answer(get_text(lang, "download"))

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, f"{safe_title}.mp3")

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'bestaudio/best',
            'quiet': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            def sync_download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            await asyncio.to_thread(sync_download)

            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                await msg.edit_text(get_text(lang, "system_error"))
                return

            with open(filepath, "rb") as f:
                audio_bytes = BytesIO(f.read())
                audio_input = InputFile(audio_bytes, filename=f"{safe_title}.mp3")
                await msg.edit_text(get_text(lang, "send"))
                await bot.send_audio(chat_id=chat_id, audio=audio_input,
                                     caption="<b>Незабывай делиться ботом з другом! - <a href='https://t.me/ytdownlad_bot'>поделиться!</a></b>",
                                     parse_mode="HTML")
                download_user(tg_id)
                await msg.delete()

        except Exception as e:
            await callback.message.answer(get_text(lang, "incorect_link"))
            print(f'{e}')

        finally:
            user_video_data.pop(chat_id, None)


@downloader.callback_query(lambda c: c.data.startswith("quality_"))
async def process_quality(callback: CallbackQuery):
    lang = check_lang(callback.from_user.id)
    tg_id = callback.from_user.id
    format_id = callback.data.split("_")[1]
    chat_id = callback.message.chat.id

    await callback.answer(get_text(lang, "inicilization"))

    data = user_video_data.get(chat_id)
    if not data:
        await callback.message.edit_text(get_text(lang, "incorect_link"))
        return

    url = data["url"]
    filename = f"{uuid.uuid4()}.mp4"

    await callback.message.delete()
    msg = await callback.message.answer(get_text(lang, "download"))

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': f"best[format_id={format_id}]",
            'merge_output_format': 'mp4',
            'quiet': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            },
        }

        try:
            def sync_download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            await asyncio.to_thread(sync_download)

            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                await msg.edit_text(get_text(lang, "system_error"))
                return

            with open(filepath, "rb") as f:
                video_bytes = BytesIO(f.read())
                video_input = InputFile(video_bytes, filename=filename)
                await msg.edit_text(get_text(lang, "send"))
                await bot.send_video(chat_id=chat_id, video=video_input)
                download_user(tg_id)
                await asyncio.sleep(1)
                await msg.delete()

        except Exception as e:
            await callback.message.edit_text(get_text(lang, "incorect_link"))
            print(f'{e}')

        finally:
            user_video_data.pop(chat_id, None)
