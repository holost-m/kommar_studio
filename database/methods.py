import sqlite3, os

DB_NAME = 'database/kommar_studio_db.db3'
DB_NAME2 = 'kommar_studio_db.db3'


class Buttons:
    @classmethod
    def answer(cls, button_name):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_select_query = """select id, type, text, url, button_name, text_answer from Buttons where button_name = ?"""
            cursor.execute(sql_select_query, (button_name,))
            lst = list(cursor.fetchone())

            # Если тип кнопки возвращающий фото
            if lst[1] == 'photos_text':
                id = lst[0]
                sql_select_query = """select tg_id from Photos where button_id = ?"""
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
            res = cursor.fetchone()
            if res:
                id = res[0]

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
                                  (tg_id, button_id)
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

    @classmethod
    def update_text(cls, button_name, new_text):
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()

            sql_update_query = """Update Buttons set text_answer = ? where button_name = ?"""
            data = (new_text, button_name)
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
    def get_tg_ids(cls) -> list:
        """
        Вернет все tg_id пользователей
        """
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

    @classmethod
    def get_id_by_tg_id(cls, tg_id: int) -> int | None:
        """
        Получить идентификатор пользователя по его tg_id
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

class NewYearQuestions:
    column_names = ('id', 'number', 'question', 'description', 'type', 'button', 'is_active')

    @classmethod
    def get_all_questions(cls) -> list[tuple]:
        """
        Получить все вопросы из таблицы NewYearQuestions, которые активны на данный момент
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NewYearQuestions WHERE is_active = 1")
            questions = cursor.fetchall()
            return questions

    @classmethod
    def get_question_by_number(cls, number: int) -> tuple:
        """
        Получить один вопрос по его номеру (проверка на active)
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NewYearQuestions WHERE number = ? AND is_active = 1", (number,))
            question = cursor.fetchone()
            return question

    @classmethod
    def get_active_question_numbers(cls) -> list[int]:
        """
        Получить все активные номера вопросов
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT number FROM NewYearQuestions WHERE is_active = 1")
            active_numbers = [row[0] for row in cursor.fetchall()]
            return active_numbers

class NewYearAnswer:
    column_names = ('id', 'user_id', 'answer')
    @classmethod
    def insert_answer(cls, user_id: int, answer: str):
        """
        Вставить новый ответ в таблицу NewYearAnswer
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO NewYearAnswer (user_id, answer) VALUES (?, ?)", (user_id, answer))
            conn.commit()

    @classmethod
    def get_answer_by_user_id(cls, user_id: int) -> tuple:
        """
        Получить данные ответа по user_id
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NewYearAnswer WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return result

    @classmethod
    def clear_table(cls):
        """
        Полная очистка таблицы NewYearAnswer. Только для тестов
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM NewYearAnswer")
            conn.commit()




if __name__ == "__main__":
    print(Users.get_all_users())



