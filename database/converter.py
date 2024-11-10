import sqlite3, os

DB_NAME = 'kommar_studio_db.db3'


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Добавление строки в таблицу Buttons
cursor.execute('''
INSERT INTO Buttons (type, text, button_name, text_answer)
VALUES (?, ?, ?, ?)
''', ('photos_text', '🎄NEW🎄 СОЗДАТЬ ВАШ НОВОГОДНИЙ ЖУРНАЛ', 'new_year', 'Новый год'))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
print('Успешно добавлены данные')
