import sqlite3, os

DB_NAME = 'database/kommar_studio_db.db3'
DB_NAME2 = 'kommar_studio_db.db3'


class Buttons:
    @classmethod
    def answer(cls, button_name):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_select_query = """select id, type, text, url, code_name, text_answer from Buttons where code_name = ?"""
            cursor.execute(sql_select_query, (button_name,))
            lst = list(cursor.fetchone())

            # Если тип кнопки возвращающий фото
            if lst[1] == 'photos_text':
                id = lst[0]
                sql_select_query = """select file from Photos where button_id = ?"""
                cursor.execute(sql_select_query, (id,))
                files = cursor.fetchall()
                lst.append(files)
            else:
                lst.append(None)
            return lst

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    @classmethod
    def get_url(cls, button_name):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_select_query = """select url from Buttons where button_name = ?"""
            cursor.execute(sql_select_query, (button_name,))
            url = cursor.fetchone()[0]

            return url

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    @classmethod
    def get_id_by_button_name(cls, button_name):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_select_query = """select id from Buttons where button_name = ?"""
            cursor.execute(sql_select_query, (button_name,))
            id = cursor.fetchone()[0]

            return id

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    @classmethod
    def save_photo(cls, button_name, photo_id):
        id = cls.get_id_by_button_name(button_name)

        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sqlite_insert_query = """INSERT INTO Photos
                                  (file, button_id)
                                  VALUES
                                  (?, ?);"""
            count = cursor.execute(sqlite_insert_query, (photo_id, id))
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    @classmethod
    def delete_photo(cls, button_name):
        id = cls.get_id_by_button_name(button_name)
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_update_query = """DELETE from Photos where button_id = ?"""
            cursor.execute(sql_update_query, (id,))
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    @classmethod
    def update_text_answer(cls, button_name, new_text_answer):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_update_query = """Update Buttons set text_answer = ? where button_name = ?"""
            data = (new_text_answer, button_name)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    @classmethod
    def update_url(cls, button_name, new_url):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_update_query = """Update Buttons set url = ? where button_name = ?"""
            data = (new_url, button_name)
            cursor.execute(sql_update_query, data)
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

class Users:
    @classmethod
    def get_tg_ids(cls):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT tg_id FROM users')

            # Получаем все строки
            tg_ids = list(map(lambda x: x[0], cursor.fetchall()))
        return tg_ids

    @classmethod
    def save_user(cls, tg_id, first_name, last_name, username, url, current_date_iso):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO users (tg_id, first_name, last_name, username, url, current_date_iso)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (tg_id, first_name, last_name, username, url, current_date_iso))
            conn.commit()

    @classmethod
    def get_all_users(cls):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return users




if __name__ == "__main__":
    print(Users.get_all_users())



