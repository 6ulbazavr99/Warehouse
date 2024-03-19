from aiogram.types import Message
from core.utils.db_connect import Request


async def get_product(message: Message, request: Request):
    products = await request.get_all_products()
    response = "\n".join(
        [f"Код товара: {product['id']}\nНазвание: {product['name']}\nКоличество: {product['quantity']}\n"
         for product in products])
    await message.answer(response)
