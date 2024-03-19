import sys
import asyncio
import logging
import contextlib
import asyncpg
from decouple import config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart

from core.handlers.basic import get_start, get_token, get_help
from core.handlers.add_product import add_product, get_code, get_name, get_quantity
from core.handlers.get_product import get_product
from core.handlers.withdraw import get_withdraw, get_code_withdraw, get_quantity_withdraw
from core.handlers.export_excel import export_to_excel

from core.middlewares.chat_action import ExampleChatActionMiddleware
from core.middlewares.db_action import DbSession

from core.utils.states_form import StepsForm
from core.utils.commands import set_commands
from core.utils.db_connect import create_database_table


token = config('BOT_TOKEN')
admin = config('ADMIN_ID')


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(admin, text='Бот остановлен!')


async def create_pool():
    return await asyncpg.create_pool(
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        database=config('DB_NAME'),
        host=config('DB_HOST'),
        port=config('DB_PORT'),
        command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token, parse_mode=ParseMode.HTML)
    await create_database_table()
    pool_connect = await create_pool()
    dp = Dispatcher()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(ExampleChatActionMiddleware())

    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    dp.message.register(get_start, CommandStart())
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(get_token, StepsForm.GET_TOKEN)
    dp.message.register(add_product, Command(commands='add'))
    dp.message.register(get_code, StepsForm.GET_CODE)
    dp.message.register(get_name, StepsForm.GET_NAME_PR)
    dp.message.register(get_quantity, StepsForm.GET_QUANTITY)
    dp.message.register(get_product, Command(commands='list'))
    dp.message.register(get_withdraw, Command(commands='withdraw'))
    dp.message.register(get_code_withdraw, StepsForm.GET_CODE_WITH)
    dp.message.register(get_quantity_withdraw, StepsForm.GET_QUANTITY_WITH)
    dp.message.register(export_to_excel, Command(commands='file'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())


# TODO: рефакт +
# TODO: понять
# TODO: рефакт
# TODO: дополнить
# TODO: структурировать
# TODO: документирование
# TODO: тест
# TODO: рефакт
