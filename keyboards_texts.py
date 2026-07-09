from aiogram.utils.keyboard import InlineKeyboardBuilder

def successful_booked_text(user_name):
    return f"{user_name}, запись подтверждена!"

unsuccessful_booked_text = "К сожалению, эта запись уже занята."

def build_slots_keyboard(free_slots_list, date):
    builder = InlineKeyboardBuilder()

    for slot in free_slots_list:
        builder.button(text=f"{slot}:00", callback_data=f"book|{slot}|{date}")
    builder.adjust(3) 
    return builder.as_markup()

def day_reminder_text(user_name, booking_time):
    return f"{user_name}, вы записаны на завтра. Время: {booking_time}"

def hour_reminder_text(user_name, booking_time):
    return f"{user_name}, скоро Ваша запись. Время: {booking_time}"