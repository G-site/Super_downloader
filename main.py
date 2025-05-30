import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from app.database import data_create, admin_create
from app.handlers import router
from app.download import downloader
from app.admin import admin


bot = Bot(token="7523888655:AAH-_AfcqfeOdiYSFXyoxnL7oRSd_1840-Q")
dp = Dispatcher()

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Меню"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="profile", description="Профиль"),
        BotCommand(command="lang", description="Язык")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def set_bot_description(bot: Bot):
    await bot.set_my_short_description(
        "🤖Скачивай видео из YouTube и других соцсетей — быстро, бесплатно и без водяных знаков!\n\nСвязаться: @orlovurasuper"
    )
    await bot.set_my_description(
        "🤖Скачивай видео из YouTube и других соцсетей — быстро, бесплатно и без водяных знаков!\n\nСвязаться: @orlovurasuper"
    )



data_create()
admin_create()


async def main():

    await set_bot_commands(bot)
    await set_bot_description(bot)

    dp.include_router(router)
    dp.include_router(downloader)
    dp.include_router(admin)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
