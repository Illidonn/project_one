from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject


from config import ADMIN_ID
from db import add_schedule


router = Router()

@router.message(Command("set_schedule"), F.from_user.id == ADMIN_ID)
async def command_set_schedule(message: Message, command: CommandObject):
    data = command.args
    if data is None:
        await message.answer("передай расписание в формате: 0(0-6: понедельник-воскресенье) 09:00-18:00(время работы) 12:00(час начала перерыва)")
        return
    day_week, working_time, break_time = data.split()
    add_schedule(int(day_week), working_time, break_time)
    await message.answer(f'{message.from_user.full_name}, расписание на выбранный день недели добавлено.')