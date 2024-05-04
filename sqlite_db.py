import sqlite3 as sl
import datetime
from xlsxwriter.workbook import Workbook


async def db_connect():
    '''Выполняет подключение к базе данных и создаёт нужные таблицы'''
    global con, cur

    con = sl.connect('data.db')
    cur = con.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                   user_name TEXT,
                   user_id BIGINT
        );
            """)
    con.commit()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY,
                    person_id BIGINT
        );
            """)
    con.commit()


# Пользователь
async def get_users():
    '''Получает всех пользователей из таблицы users'''
    users = cur.execute("SELECT * FROM users").fetchall()
    return users


async def get_person(user_id: int):
    '''Получает одного пользователя по message.chat.id пользователя'''
    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id};").fetchall()
    return user


async def push_data_in_people(user_name: str, user_id: int):
    '''Создаёт одного пользователя по введённым данным'''
    data = (user_name, user_id)
    cur.execute(
        "INSERT INTO users(user_name, user_id) VALUES (?, ?);",
        data)
    con.commit()


# Админы
async def get_admins():
    '''Получает всех администраторов из таблицы admins'''
    admins = cur.execute("SELECT * FROM admins").fetchall()
    return admins


async def create_admin(person_id: int):
    '''Создаёт одного администратора по введённым данным'''
    cur.execute(f"INSERT INTO admins(person_id) VALUES ({person_id});")
    con.commit()


async def get_people():
    users = await get_users()
    workbook = Workbook('people.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "№")
    worksheet.write(0, 1, "id пользователя")
    worksheet.write(0, 2, "Имя в телеграм")
    for i, claim_id in enumerate(users):
        worksheet.write(i + 1, 0, claim_id[0])
        worksheet.write(i + 1, 1, claim_id[2])
        worksheet.write(i + 1, 2, '' + (claim_id[1] if claim_id[1] != None else ''))
    workbook.close()