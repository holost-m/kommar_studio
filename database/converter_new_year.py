import sqlite3, os

DB_NAME = 'kommar_studio_db.db3'


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Создание NewYearQuestions
cursor.execute('''
CREATE TABLE IF NOT EXISTS NewYearQuestions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER, -- номер вопроса по порядку в анкете
    question TEXT, -- короткий вопрос
    description TEXT, -- описание вопроса для пользователя
    type TEXT, -- тип ответа photo_text/text/press_button
    button TEXT, -- текст на кнопке, которую нужно нажать для следующего вопроса
    is_active INTEGER -- 1 - активный вопрос, 0 - вопрос в архиве
);
''')
conn.commit()

#  Заполнение NewYearQuestions
try:
    cursor.execute('''
    INSERT INTO NewYearQuestions (number, question, description, type, button, is_active) VALUES
    (1, 'Как вы оцениваете прошедший год?', 'Поделитесь своими впечатлениями о прошедшем годе.', 'press_button', 'Далее', 1),
    (2, 'Какие события были самыми значимыми?', 'Расскажите о самых значимых событиях прошедшего года.', 'press_button', 'ОК, продолжим', 1),
    (3, 'Какие цели вы достигли в этом году?', 'Поделитесь своими достижениями за прошедший год.', 'press_button', 'Поехали', 1),
    (4, 'Какие у вас планы на следующий год?', 'Расскажите о своих планах на следующий год.', 'text', '', 1),
    (5, 'Нажмите кнопку, чтобы перейти к следующему вопросу.', 'Нажмите кнопку "Далее".', 'press_button', 'Далее', 1),
    (6, 'Какие темы вам интересны?', 'Выберите темы, которые вам интересны.', 'text', '', 1),
    (7, 'Поделитесь фото вашего любимого места для чтения.', 'Загрузите фото вашего любимого места для чтения.', 'photo_text', '', 1),
    (8, 'Как вы оцениваете качество нашего журнала?', 'Оцените качество нашего журнала по шкале от 1 до 10.', 'text', '', 1),
    (9, 'Нажмите кнопку, чтобы перейти к следующему вопросу.', 'Нажмите кнопку "Далее".', 'press_button', 'Далее', 1),
    (10, 'Есть ли у вас предложения по улучшению журнала?', 'Поделитесь своими предложениями по улучшению журнала.', 'text', '', 1);
    ''')
    conn.commit()
    print('Успешно добавлены данные NewYearQuestions!')
except sqlite3.Error as e:
    print(f'Ошибка при добавлении данных: {e}')


try:
    # Создание NewYearAnswers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NewYearAnswer
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, -- FK на id пользователя
        answer TEXT, -- json-строка
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')
    conn.commit()
    print('Успешно добавлены данные NewYearAnswer!')
except sqlite3.Error as e:
    print(f'Ошибка при добавлении данных: {e}')


conn.close()