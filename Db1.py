import psycopg2


def connect_db():
    """Подключение к базе данных"""
    con = psycopg2.connect(
        database="d5ooudpafo8gka",
        user="xepxpqywxklads",
        password="56d9d97426002b5c458acf4847dd36e3c149131255887e0687d875d38b3c102e",
        host="ec2-107-22-33-173.compute-1.amazonaws.com",
        port="5432")
    return con


def init_db():
    """Открыть курсор дл явыполнения операций с базой данных"""
    con = connect_db()
    cur = con.cursor()
    """Выполните команду: это создаст новую таблицу"""
    cur.execute(""" CREATE TABLE user_project (
            user_id    INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            code_name TEXT NOT NULL,
            text_start TEXT NOT NULL,
            time_start TEXT NOT NULL,
            text_and TEXT NOT NULL,
            time_and TEXT NOT NULL);""")

    con.commit()
    con.close()


def add_message(user_id: int, first_name: str, code_name: str, text_start: str, time_start: str, text_and: str,
                time_and: str):
    """Добавить строку"""
    con = connect_db()
    c = con.cursor()
    c.execute(
        'INSERT INTO user_project (user_id, first_name, code_name, text_start, time_start, text_and, time_and) VALUES (%s ,%s, %s, %s, %s, %s, %s)',
        (user_id, first_name, code_name, text_start, time_start, text_and, time_and))
    con.commit()
    con.close()


def update_data(code_name: str, text_and: str, time_and: str):
    """Обновить данные в строке"""
    con = connect_db()
    c = con.cursor()
    c.execute('UPDATE user_project set text_and = %s, time_and =%s  where code_name = %s',
              (text_and, time_and, code_name))
    con.commit()
    con.close()
    # print("Обновлено")


def list_message(first_name: str):
    """Показать список все строки данных по имени"""
    con = connect_db()
    c = con.cursor()
    c.execute(
        'SELECT code_name, text_start, time_start, text_and, time_and FROM user_project WHERE first_name = %s ',
        (first_name,))
    return c.fetchall()


def name_message(name):
    """Показать по названию изделия или по артикулу"""
    con = connect_db()
    c = con.cursor()
    c.execute(
        f"SELECT first_name, code_name, text_start, time_start, text_and, time_and FROM user_project where text_start like '%{name}'"
        f" or code_name like '%{name}' ")
    quantity = c.fetchall()
    return quantity


def delete_message(code_name: str):
    """Удалить данные по артикулу и назваиню"""
    con = connect_db()
    c = con.cursor()
    c.execute('DELETE from user_project WHERE code_name= %s', (code_name,))
    con.commit()
    con.close()


def message(first_name):
    """Перебрать все данные списка"""
    f = list_message(first_name=first_name)
    list1 = []
    for i in f:
        list1.append(f"{i}/n")
    return list1


def date(first_name):
    f = list_message(first_name=first_name)
    # print(f[0])
    datetime = f[0]
    # print(datetime[1])
    return datetime[1]


if __name__ == '__main__':
    '''init_db()'''
    # delete_message("10046")
    # add_message(1268358424,'Sergey', '10046', 'Скамейка Урсула', '2020.08.03-12:17', 'Завершен', '2020.08.04-10:44')
    # projects = list_message("Sergey")

    # print(name_message("Скамейка Урсулa"))
    # print(message("Sergey"))
