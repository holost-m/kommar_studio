import sqlite3
import os
from datetime import datetime

# Путь к исходной базе данных
DB_NAME = 'kommar_studio_db.db3'

# Папка для сохранения дампов
DUMP_FOLDER = 'dumps'

# Убедитесь, что папка для дампов существует
if not os.path.exists(DUMP_FOLDER):
    os.makedirs(DUMP_FOLDER)

# Получение текущей даты и времени
now = datetime.now()
timestamp = now.strftime("%d.%m.%Y_%H:%M")

# Имя файла дампа
dump_filename = f'dump_{timestamp}.sql'
dump_path = os.path.join(DUMP_FOLDER, dump_filename)

# Функция для создания дампа базы данных
def create_dump(db_name, dump_path):
    conn = sqlite3.connect(db_name)
    with open(dump_path, 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    conn.close()

# Создание дампа
create_dump(DB_NAME, dump_path)

print(f'Дамп базы данных создан: {dump_path}')