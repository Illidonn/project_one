from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import date
import html


DAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


def successful_booked_text(user_name):
    return f"{html.escape(user_name)}, запись подтверждена!"

unsuccessful_booked_text = "К сожалению, эта запись уже занята."

def build_slots_keyboard(free_slots_list, iso_date):
    builder = InlineKeyboardBuilder()

    for slot in free_slots_list:
        builder.button(text=slot, callback_data=f"book|{slot}|{iso_date}")
    builder.adjust(3) 
    return builder.as_markup()

def build_dates_keyboard(free_days_list):
    builder = InlineKeyboardBuilder()

    for d in free_days_list:
        current = date.fromisoformat(d)
        builder.button(text=f"{DAYS_RU[current.weekday()]} {current.strftime('%d/%m')}", callback_data=f"day|{d}")
    builder.adjust(3) 
    return builder.as_markup()

def day_reminder_text(user_name, booking_time):
    return f"{html.escape(user_name)}, Вы записаны на завтра. Время: {html.escape(booking_time)}"

def hour_reminder_text(user_name, booking_time):
    return f"{html.escape(user_name)}, скоро Ваша запись. Время: {html.escape(booking_time)}"