from aiogram.utils.keyboard import InlineKeyboardBuilder
import html

def successful_booked_text(user_name):
    return f"{html.escape(user_name)}, запись подтверждена!"

unsuccessful_booked_text = "К сожалению, эта запись уже занята."

def build_slots_keyboard(free_slots_list, date):
    builder = InlineKeyboardBuilder()

    for slot in free_slots_list:
        builder.button(text=f"{slot}:00", callback_data=f"book|{slot}|{date}")
    builder.adjust(3) 
    return builder.as_markup()

def day_reminder_text(user_name, booking_time):
    return f"{html.escape(user_name)}, Вы записаны на завтра. Время: {html.escape(booking_time)}"

def hour_reminder_text(user_name, booking_time):
    return f"{html.escape(user_name)}, скоро Ваша запись. Время: {html.escape(booking_time)}"