import asyncio
import logging

from db import get_bookings_for_day_reminder, get_bookings_for_hour_reminder, mark_day_reminder_sent, mark_hour_reminder_sent
from keyboards_texts import day_reminder_text, hour_reminder_text


async def run_reminders(bot):
    while True:
        for booking in get_bookings_for_day_reminder():
            booking_id, user_id, user_name, _, b_time = booking
            try:
                text = day_reminder_text(user_name, b_time)
                await bot.send_message(user_id, text)
                mark_day_reminder_sent(booking_id)
            except Exception:
                logging.exception("Не удалось отправить дневное напоминание, booking_id=%s", booking_id)

        for booking in get_bookings_for_hour_reminder():
            booking_id, user_id, user_name, _, b_time = booking
            try:
                text = hour_reminder_text(user_name, b_time)
                await bot.send_message(user_id, text)
                mark_hour_reminder_sent(booking_id)
            except Exception:
                logging.exception("Не удалось отправить часовое напоминание, booking_id=%s", booking_id)

        await asyncio.sleep(600)