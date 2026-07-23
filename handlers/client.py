from aiogram import Router, F
from aiogram.types import CallbackQuery, Message 
from aiogram.filters import Command
from datetime import date


from db import add_booking, get_free_slots, get_free_dates
from keyboards_texts import build_slots_keyboard, build_dates_keyboard

from keyboards_texts import successful_booked_text, unsuccessful_booked_text


router = Router()

@router.callback_query(F.data.startswith("book|"))
async def booking_handler(query: CallbackQuery):
    data = query.data.split("|")
    if len(data) != 3:
        await query.answer("Что-то пошло не так, обновите запрос.")
        return
    time_for_book, date_for_book = data[1], data[2]
    if date_for_book not in get_free_dates():
        await query.answer("Дата больше недоступна, отправьте /book заново.", show_alert=True)
        return
    if time_for_book not in get_free_slots(date_for_book):
        await query.answer("Слот уже заняли, отправьте /book заново.", show_alert=True)
        return
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    result = add_booking(user_id, user_name, date_for_book, time_for_book)
    await query.answer()
    if result:
        await query.message.edit_text(successful_booked_text(user_name))
    else:
        await query.message.answer(unsuccessful_booked_text)

@router.message(Command("book"))
async def command_book(message: Message):
    free_dates_list = get_free_dates()
    if not free_dates_list:
        await message.answer("Свободных дат на ближайшее время нет, попробуйте позже.")
        return
    dates_keyboard = build_dates_keyboard(free_dates_list)
    return await message.answer("Выберите подходящую дату:", reply_markup=dates_keyboard)

@router.callback_query(F.data.startswith("day|"))
async def booking_date_handler(query: CallbackQuery):
    parts = query.data.split("|")
    if len(parts) != 2:
        await query.answer("Не удалось обработать выбор, отправьте /book заново")
        return
    _, iso_date = parts
    if iso_date not in get_free_dates():
        await query.answer("Дата больше недоступна, обновите запрос.", show_alert=True)
        return
    await query.answer()

    free_slots = get_free_slots(iso_date)

    slots_keyboard = build_slots_keyboard(free_slots, iso_date)
    selected_date = date.fromisoformat(iso_date)
    await query.message.edit_text(f"Свободные слоты на {selected_date.strftime('%d/%m')}:", reply_markup=slots_keyboard)
