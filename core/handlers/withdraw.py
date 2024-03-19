from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.utils.states_form import StepsForm
from core.utils.db_connect import Request


async def get_withdraw(message: Message, state: FSMContext):
    await message.answer(f'Введите код товара для вычета (код должен быть только целым числом)')
    await state.set_state(StepsForm.GET_CODE_WITH)


async def get_code_withdraw(message: Message, state: FSMContext):
    await message.answer(f'Код товара: {message.text}\r\nТеперь введите количество')
    await state.update_data(code=message.text)
    await state.set_state(StepsForm.GET_QUANTITY_WITH)


async def get_quantity_withdraw(message: Message, state: FSMContext, request: Request):
    try:
        context_data = await state.get_data()
        code = int(context_data.get('code'))
        await request.withdraw(code, int(message.text), message)

        data = f'Количество "{message.text}" из товара с кодом "{code}" успешно вычтено.'
        await message.answer(data)

        await state.clear()
    except ValueError:
        await message.answer('Неверно указаны данные.')
