from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
import asyncio
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database import download_user, check_admin
from app.language import get_text
import sqlite3
admin = Router()
from aiogram.types import BufferedInputFile

import app.links as ln

import os
from aiogram.utils.keyboard import InlineKeyboardBuilder



from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError


class Add_admin(StatesGroup):
    id = State()


from app.database import add_admin, basic_static

import pandas as pd
import io
import openpyxl
import re



from app.language import get_text


def check_lang(user_id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("""SELECT lang FROM users WHERE tg_id = ?""", [user_id])
    lang = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return lang[0] if lang else "ru"


@admin.message(Command('admin'))
async def admin_panel(message: Message):
    lang = check_lang(message.from_user.id)
    tg_id = message.from_user.id
    name = message.from_user.first_name
    admin_status, range = check_admin(tg_id)

    if admin_status == True:
        if range == 0:
            await message.answer(f"Добро пожаловать в админ-панель, <b>{name}</b>!", reply_markup=ln.admin_panel, parse_mode="HTML")
        else:
            await message.answer(f"Добро пожаловать в админ-панель, <b>{name}</b>!", reply_markup=ln.creator_panel, parse_mode="HTML")
    else:
        await message.answer(get_text(lang, "admin_status"))


@admin.callback_query(F.data == 'admin')
async def admin_panelka(callback: CallbackQuery):
    tg_id = callback.from_user.id
    name = callback.from_user.first_name
    range = check_admin(tg_id)
    if range == 0:
        await callback.message.edit_text(f"Добро пожаловать в админ-панель, <b>{name}</b>!", reply_markup=ln.admin_panel, parse_mode="HTML")
    else:
        await callback.message.edit_text(f"Добро пожаловать в админ-панель, <b>{name}</b>!", reply_markup=ln.creator_panel, parse_mode="HTML")


@admin.callback_query(F.data == 'add_admin')
async def admin_add1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Add_admin.id)
    await callback.message.edit_text(f"Добавления администратора!\n<b>Внимание!!!\nДобавляйте лишь провереных пользователей!</b> ", reply_markup=ln.come_admin, parse_mode="HTML")


@admin.message(Add_admin.id)
async def admin_add2(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    name, be_admin = add_admin(data['id'])
    if not be_admin:
        await message.answer(f"Админ <b>{name}</b> добавлен!", reply_markup=ln.come_admin, parse_mode="HTML")
    else:
        await message.answer(f"Админ <b>{name}</b> уже добавлен!", reply_markup=ln.come_admin, parse_mode="HTML")
    await state.clear()


@admin.callback_query(F.data == 'static')
async def admin_static(callback: CallbackQuery):
    users, rus, eng, downloads = basic_static()
    await callback.message.edit_text(f"Общая статистика:\nКоличество пользователей: <b>{users}</b>\nRU: <b>{rus}</b> EN: <b>{eng}</b>\nКоличество скачиваний: <b>{downloads}</b>", reply_markup=ln.static_panel, parse_mode="HTML")


@admin.callback_query(F.data == 'static_download')
async def static_download(callback: CallbackQuery):
    conn = sqlite3.connect("database.db")
    
    # Читаем таблицу в DataFrame
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    
    # Создаём Excel в памяти (в байтах)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)
    file = BufferedInputFile(output.read(), filename="data.xlsx")
    # Отправляем файл пользователю
    await callback.message.answer_document(
        document=file,
        caption="✔ Полная статистика"
    )
    await callback.answer()


@admin.message(F.text.startswith("#\n"))
async def broadcast_news(message: Message):
    text = message.text
    tg_id = message.from_user.id

    # Розпізнаємо ru і en частини
    match_ru = re.search(r"ru:\s*(.*?)\s*(?:en:|$)", text, re.DOTALL)
    match_en = re.search(r"en:\s*(.*)", text, re.DOTALL)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id FROM admins WHERE tg_id = ?", [tg_id])
    if cursor.fetchone() is None:
        pass
    else:
        conn.close()
        if not match_ru or not match_en:
            await message.answer("⚠ Неверный формат!\n Пример:\n# перенос\nru: текст\nперенос\nen: текст")
            return

        ru_text = match_ru.group(1).strip()
        en_text = match_en.group(1).strip()

    # Підключення до бази
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tg_id, lang FROM users")
        users = cursor.fetchall()
        conn.close()

        sent = 0
        for tg_id, lang in users:
            try:
                text_to_send = ru_text if lang == "ru" else en_text
                await message.bot.send_message(
                    chat_id=tg_id,
                    text=text_to_send,
                    parse_mode=ParseMode.HTML
                )
                sent += 1
            except TelegramAPIError as e:
                print(f"Ошибка, не всем отправлено, {e}")

        await message.answer(f"✅ Отправлено {sent} пользователям!")


@admin.callback_query(F.data == 'sample')
async def sample_panel(callback: CallbackQuery):
    await callback.message.edit_text("Меню специальных шаблонов!", reply_markup=ln.sample_panel)


@admin.callback_query(F.data == 'subscribe')
async def subscribe(callback: CallbackQuery):
    tg_id = callback.from_user.id
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id, lang FROM users")
    users = cursor.fetchall()
    conn.close()

    sent = 0
    for tg_id, lang in users:
        try:
            await callback.bot.send_message(
                chat_id=tg_id,
                text=get_text(lang, "subscribe"),
                parse_mode=ParseMode.HTML,
                reply_markup=ln.subscribe(lang)
            )
            sent += 1
        except TelegramAPIError as e:
            print(f"Ошибка, не всем отправлено, {e}")
    await callback.answer(f"✅ Отправлено {sent} пользователям!")


@admin.callback_query(F.data == 'share')
async def share(callback: CallbackQuery):
    tg_id = callback.from_user.id
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id, lang FROM users")
    users = cursor.fetchall()
    conn.close()

    sent = 0
    for tg_id, lang in users:
        try:
            await callback.bot.send_message(
                chat_id=tg_id,
                text=get_text(lang, "share"),
                parse_mode=ParseMode.HTML,
                reply_markup=ln.share(lang)
            )
            sent += 1
        except TelegramAPIError as e:
            print(f"Ошибка, не всем отправлено, {e}")
    await callback.answer(f"✅ Отправлено {sent} пользователям!")


@admin.callback_query(F.data == 'update')
async def update(callback: CallbackQuery):
    tg_id = callback.from_user.id
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id, lang FROM users")
    users = cursor.fetchall()
    conn.close()

    sent = 0
    for tg_id, lang in users:
        try:
            await callback.bot.send_message(
                chat_id=tg_id,
                text=get_text(lang, "update"),
                parse_mode=ParseMode.HTML
            )
            sent += 1
        except TelegramAPIError as e:
            print(f"Ошибка, не всем отправлено, {e}")
    await callback.answer(f"✅ Отправлено {sent} пользователям!")