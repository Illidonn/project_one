from aiogram import Router, F
from aiogram.types import CallbackQuery, Message 
from aiogram.filters import Command, CommandObject

from db import add_booking, get_free_slots
from keyboards_texts import build_slots_keyboard

from keyboards_texts import successful_booked_text, unsuccessful_booked_text


router = Router()

@router.callback_query(F.data.startswith("book|"))
async def booking_handler(query: CallbackQuery):
    data = query.data.split("|")
    time_for_book, date_for_book = f"{data[1]}:00", data[2]
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    result = add_booking(user_id, user_name, date_for_book, time_for_book)
    await query.answer()
    if result:
        await query.message.answer(successful_booked_text(user_name))
    else:
        await query.message.answer(unsuccessful_booked_text)

@router.message(Command("book"))
async def command_book(message: Message, command: CommandObject):
    date = str(command.args)
    if date is None:
        await message.answer("укажи дату в формате ГГГГ-ММ-ДД")
        return
    free_slots = get_free_slots(date)
    if not free_slots:
        await message.answer("Всё занято/выходной.")
    else:
        test_keyboard = build_slots_keyboard(free_slots, date)
        await message.answer("свободные слоты:", reply_markup=test_keyboard)