import psycopg2


"""Подключение к базе данных"""
con = psycopg2.connect(
    database="dcjb1qat671637",
    user="dvhyumkmxxkpch",
    password="70821ee62bbcf15bbe02e983f761eb24939ebcf43c7966e4767ff0bbe83f8c92",
    host="ec2-54-217-204-34.eu-west-1.compute.amazonaws.com",
    port="5432")



def init_db():
    """Открыть курсор дл явыполнения операций с базой данных"""
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


def add_message(user_id: int, first_name: str,code_name:str, text_start: str,time_start: str, text_and: str, time_and: str):
    """Добавить строку"""
    c = con.cursor()
    c.execute('INSERT INTO user_project (user_id, first_name, code_name, text_start, time_start, text_and, time_and) VALUES (%s ,%s, %s, %s, %s, %s, %s)',
              (user_id, first_name,code_name, text_start, time_start, text_and, time_and))
    con.commit()

def update_data(code_name: str,text_and: str,time_and:str):
    """Обновить данные в строке"""
    c = con.cursor()
    c.execute('UPDATE user_project set text_and = %s, time_and =%s  where code_name = %s',
              (text_and, time_and, code_name))
    con.commit()
    #print("Обновлено")

def list_message(first_name: str):
    """Показать список все строки данных по имени"""
    c = con.cursor()
    c.execute('SELECT first_name, code_name, text_start, time_start, text_and, time_and FROM user_project WHERE first_name = %s ', (first_name,))
    return c.fetchall()

def quantity_message(first_name: str):
    """Показать последние 5 строк"""
    c = con.cursor()
    c.execute('SELECT first_name, time, text_start FROM user_project WHERE first_name= %s', (first_name,))
    con.commit()
    quantity = c.fetchall()[-5:]
    return quantity

def delete_message(code_name: str):
    """Удалить данные по артикулу и назваиню"""
    c = con.cursor()
    c.execute('DELETE from user_project WHERE code_name= %s',(code_name,))
    con.commit()


def message(first_name):
    """Перебрать все данные списка"""
    f = list_message(first_name=first_name)
    list1 = []
    for i in f:
        list1.append(f"{i}/n")
    return list1


def date(first_name):
    f = list_message(first_name=first_name)
    #print(f[0])
    datetime = f[0]
    #print(datetime[1])
    return datetime[1]


if __name__ == '__main__':
    init_db()
    #delete_message("1109-Столб навигации Вега")

    #print(list_message("Sergey"))
    #print(message("Sergey"))

    con.close()