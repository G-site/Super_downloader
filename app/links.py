from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)

from app.language import get_text


lang = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='🇷🇺Руский', callback_data='lang_ru')
], [InlineKeyboardButton(text='🇬🇧English', callback_data='lang_en')]])


def start_menu(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_profile"), callback_data="profile")],
        [InlineKeyboardButton(text=get_text(lang, "lets_go"), callback_data="lets_go")],
        [InlineKeyboardButton(text=get_text(lang, "btn_help"), callback_data="help")]
    ])


def help_menu(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_use_help"), url="https://t.me/super_downloader_chanel")],
        [InlineKeyboardButton(text=get_text(lang, "btn_creator"), url="https://t.me/orlovurasuper")],
        [InlineKeyboardButton(text=get_text(lang, "btn_index"), callback_data="start")]
    ])


def profile_menu(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_index"), callback_data="start")]
    ])


admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Статистика', callback_data='static')],
    [InlineKeyboardButton(text='Шаблоны', callback_data='sample')],
    [InlineKeyboardButton(text='Добавить новость', callback_data='add_news')],
    [InlineKeyboardButton(text='Союз админов', callback_data='admin')], #url
])

creator_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Статистика', callback_data='static')],
    [InlineKeyboardButton(text='Шаблоны', callback_data='sample')],
    [InlineKeyboardButton(text='Добавить новость', callback_data='add_news')],
    [InlineKeyboardButton(text='Управление администрацией', callback_data='control_admin')],
    [InlineKeyboardButton(text='Добавление админов', callback_data='add_admin')],
    [InlineKeyboardButton(text='Союз админов', callback_data='admin')],  #url
])

static_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Скачать таблицу активности', callback_data='static_download')],
    [InlineKeyboardButton(text='На главную', callback_data='admin')]
])

come_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='На главную', callback_data='admin')]
])

sample_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписка', callback_data='subscribe')],
    [InlineKeyboardButton(text='Поделиться', callback_data='share')],
    [InlineKeyboardButton(text='Тех-перерыв', callback_data='update')],
    [InlineKeyboardButton(text='На главную', callback_data='admin')]
])


def subscribe(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_subscribe"), url="https://t.me/super_downloader_chanel")]
    ])


def share(lang):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text(lang, "btn_share"),
                    switch_inline_query=""
                )
            ]
        ]
    )
    return keyboard