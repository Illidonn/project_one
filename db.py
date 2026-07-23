import sqlite3


from contextlib import closing
from datetime import date, datetime, timedelta


from config import SCHEDULE_RESERVATIONS


def init_db():
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        with con:
            con.execute("""CREATE TABLE IF NOT EXISTS reservations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        user_name TEXT,
                        date TEXT,
                        time TEXT,
                        reminded_day INTEGER DEFAULT 0,
                        reminded_hour INTEGER DEFAULT 0,
                        UNIQUE(date, time)
                        );""")
            con.execute("""CREATE TABLE IF NOT EXISTS schedule (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        day_week INTEGER,
                        working_time TEXT,
                        break_time TEXT,
                        UNIQUE (day_week)
                        );""")

def add_booking(user_id, user_name, date, time):
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        with con:
            sql_query = """INSERT INTO reservations (user_id, user_name, date, time)
                            VALUES (?, ?, ?, ?) 
                            """
            try:
                con.execute(sql_query, (user_id, user_name, date, time,))
                return True
            except sqlite3.IntegrityError:
                return False
            
def get_free_dates():
    start_date = date.today()
    check_dates = [(start_date + timedelta(days=i)).isoformat() for i in range(12)]

    free_dates_list = []
    for day in check_dates:
        slots = get_free_slots(day)
        if slots:
            free_dates_list.append(day)
    return free_dates_list

def get_free_slots(iso_date):
    day_week = datetime.fromisoformat(iso_date).weekday()
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        row = con.execute("SELECT working_time, break_time FROM schedule WHERE day_week = ?",(day_week,)).fetchone()
        if row is None:
            return []          # выходной
        working_time, break_time_str = row

    start_string, finish_string = working_time.split("-") #получаем начало/конец рабочего дня в строках
    start, finish = int(start_string.split(":")[0]), int(finish_string.split(":")[0]) #распарсиваем начало/конец в integer для прогона

    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        booked_tuples = con.execute("""SELECT time
        FROM reservations
        WHERE date = ?;""", (iso_date, )).fetchall()

    booked_list = [item for t in booked_tuples for item in t]
    booked_list_int = [int(str_time.split(":")[0]) for str_time in booked_list] #список числовых занятых часов
   
    free = set(range(start, finish)) - set(booked_list_int)
    # TODO: перерыв пока обязателен (см. /set_schedule). Ветка задел под опциональный обед.
    if break_time_str is not None:
        free -= {int(break_time_str.split(":")[0])}
    if iso_date == date.today().isoformat():
        now_hour = datetime.now().hour
        free -= set(range(0, now_hour + 1))
    return [f"{h:02d}:00" for h in sorted(free)]

def add_schedule(day_week, working_time, break_time):
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        with con:

            con.execute("""INSERT INTO schedule (day_week, working_time, break_time)
                           VALUES (?, ?, ?)
                           ON CONFLICT(day_week) DO UPDATE SET 
                           working_time = excluded.working_time,
                           break_time = excluded.break_time 
                           """, (day_week, working_time, break_time))

def get_bookings_for_day_reminder():
    tomorrow = str(date.today() + timedelta(days=1))
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        data = con.execute("""SELECT id, user_id, user_name, date, time FROM reservations 
                            WHERE date = ? AND reminded_day = 0""", (tomorrow, )).fetchall()
        return data
    
def mark_day_reminder_sent(booking_id):
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        with con:
            con.execute("""UPDATE reservations
                        SET reminded_day = 1
                        WHERE id = ?""", (booking_id, ))

def get_bookings_for_hour_reminder():
    moment = datetime.now()
    now = moment.strftime("%Y-%m-%d %H:%M")
    deadline = (moment + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        data = con.execute("""SELECT id, user_id, user_name, date, time FROM reservations 
                            WHERE date || ' ' || time BETWEEN ? AND ? AND reminded_hour = 0""", (now, deadline)).fetchall()
        return data

def mark_hour_reminder_sent(booking_id):
    with closing(sqlite3.connect(SCHEDULE_RESERVATIONS)) as con:
        with con:
            con.execute("""UPDATE reservations
                        SET reminded_hour = 1
                        WHERE id = ?""", (booking_id, ))
    