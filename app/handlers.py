from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.database import check_user
import app.links as ln
from app.language import get_text
import sqlite3
router = Router()

from app.database import set_user

def check_lang(user_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT lang FROM users WHERE tg_id = ?""", [user_id])
    lang = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return lang[0] if lang else "ru"
    
   

def set_user_lang(user_id, lang):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute('''UPDATE users SET lang = ? WHERE tg_id = ?''', (lang, user_id))
    db.commit()
    cursor.close()
    db.close()
   

@router.message(Command('start'))
async def start(message: Message):
    if message.from_user:
        res = set_user(message.from_user.id, message.from_user.username,  message.from_user.first_name)
        if res == True:
            await message.reply("Выберите язык / Choose the language", reply_markup=ln.lang)
            lang = check_lang(message.from_user.id)
            await message.answer(get_text(lang, "start"), reply_markup=ln.start_menu(lang))
        else:
            lang = check_lang(message.from_user.id)
            await message.answer(get_text(lang, "start"), reply_markup=ln.start_menu(lang))

@router.callback_query(F.data.startswith("lang_"))
async def lang_choose(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]
    set_user_lang(callback.from_user.id, lang_code)
    text = {
        "en": "✅ You have selected English.",
        "ru": "✅ Вы выбрали русский язык."
    }.get(lang_code, "✅ Language selected.")
    await callback.message.edit_text(text)

@router.message(Command('lang'))
async def lang(message: Message):
    await message.reply("Выберите язык / Choose the language", reply_markup=ln.lang)

@router.message(Command('help'))
async def help(message: Message):
    lang = check_lang(message.from_user.id)
    await message.answer(get_text(lang, "help"), reply_markup=ln.help_menu(lang))

@router.callback_query(F.data == 'help')
async def help_call(callback: CallbackQuery):
    lang = check_lang(callback.from_user.id)
    await callback.message.edit_text(get_text(lang, "help"), reply_markup=ln.help_menu(lang))

@router.callback_query(F.data == 'start')
async def start_call(callback: CallbackQuery):
    lang = check_lang(callback.from_user.id)
    await callback.message.edit_text(get_text(lang, "start"), reply_markup=ln.start_menu(lang))

@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    lang = check_lang(callback.from_user.id)
    profile_text = get_text(lang, "profile")
    set_user(callback.from_user.id, callback.from_user.username,  callback.from_user.first_name)
    name, balance, status = check_user(callback.from_user.id, callback.from_user.username, callback.from_user.first_name)
    name = name[0] if name else "Без имени"
    status = status[0] if status else "User"
    balance = balance[0] if balance else 0
    text = profile_text.format(name=name, balance=balance, lang=lang, status=status)
    await callback.message.edit_text(text, reply_markup=ln.profile_menu(lang))

@router.callback_query(F.data == 'lets_go')
async def lets_go(callback: CallbackQuery):
    lang = check_lang(callback.from_user.id)
    await callback.message.edit_text(get_text(lang, "lets_go_txt"))

