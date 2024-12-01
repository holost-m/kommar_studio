from aiogram.fsm.state import default_state, State, StatesGroup
from database.methods import NewYearQuestions
import redis
import json

red = redis.Redis(host='localhost', port=6379, db=0)
red.flushdb()

class UserDict:
    """
        Обертка над словарем, который хранится в редис по ключу.
        Абстрагируемся от редис и работаем с ним, будто с обычным словарем питон.
        Он нужен для того, чтобы при записи значений в этот словарь,
        они автоматически обновлялись в редис.
        По идее словарь на два ключа: 'state', 'answers'
    """

    def __init__(self, redis_dict, user_id: int, user_dict: dict):
        self.redis_dict = redis_dict
        self.user_id: int = user_id
        self.user_dict: dict = user_dict

    def __getitem__(self, key):
        return self.user_dict.get(key)

    def __setitem__(self, key, value):
        self.user_dict[key] = value
        self.redis_dict[self.user_id] = self.user_dict

    def __str__(self):
        return str(self.user_dict)



class RedisDict:
    """
    Обертка над словарем, который хранится в редис по ключу.
    Абстрагируемся от редис и работаем с ним, будто с обычным словарем питон.
    При инициализации принимаем переменную подключения к редис.
    У нас это red
    """
    def __init__(self, red: redis.Redis):
        self.red: redis.Redis = red

    def __getitem__(self, user_id: int) -> dict:
        """
        Получает значение по ключу.
        Если ключ не существует, вызывает KeyError.
        """
        #  получили словарь по ключу
        value = self.red.get(str(user_id))

        if value:
            # десериализовали словарь и можем с ним работать
            simple_dict: dict = json.loads(value)

            # А вернем мы словарь UserDict, что при записи значений в него
            # они записывались в редис
            user_dict: UserDict = UserDict(self, user_id, simple_dict)

            return user_dict
        else:
            return None

    def __setitem__(self, user_id: int, value: dict):
        """
        Устанавливает значение для ключа.
        Если ключ уже существует, обновляет его значение.
        """
        new_value = json.dumps(value)
        self.red.set(str(user_id), new_value)




class FSM:
    """
    Класс машины состояний.
    Внутри этот класс подлкючен к редис и может работать с ней как со словарем.
    Отвечает за получение и изменение состояний пользователя и запись его ответов
    """
    def __init__(self, redis_dict: RedisDict):
        self.redis_dict: RedisDict = redis_dict
        self.update_states()  # получаем список состояний

    def update_states(self):
        """
        Получаем состояния из БД. Состояния это номера вопросов
        """
        question_list = list(map(int, NewYearQuestions.get_active_question_numbers()))
        question_list.append(0)
        self.states_list = sorted(question_list)
        self.first_state = self.states_list[0]
        self.last_state = self.states_list[-1] # последнее состояние - вопросы пройдены
        self.states_list.pop()

    def create_answer_tmpl(self, user_id: int):
        """
        Создаем шаблон словаря, который хранится в редис по id пользователя
        Берем его из БД
        """
        self.all_questions = NewYearQuestions.get_all_questions()
        self.answer_tmpl = {
                'date_start': '',
                'date_end': '',
                'body': {}
                }
        for question in self.all_questions:
            number = question[1]
            new_answer = {'id': question[0],
                          'question': question[2],
                          'type': question[4],
                          'text_answer': '',
                          'photos': []}
            self.answer_tmpl['body'][number] = new_answer

        self.redis_dict[user_id] = self.answer_tmpl

    def get_state(self, user_id: int):
        state = self.redis_dict[user_id]
        if state is None:
            return None
        else:
            return self.redis_dict[user_id]['state']

    def is_correct_state(self, user_id: int):
        state = self.get_state(user_id)
        print(state, self.states_list)
        return state in self.states_list

    def is_last_state(self, user_id: int):
        state = self.get_state(user_id)
        return state == self.last_state

    def next_state(self, user_id: int):
        """
        Возможны три случая:
        1) состояние пользователя None - запишем ему первое состояние
        2) состояние пользователя из списка возможных состояний - тогда + 1
        3) состояние пользователя - последнее состояние - тогда тоже + 1
        """
        user_state = self.get_state(user_id)

        # если нет состояния, то инициализируем его для пользователя
        if user_state is None:
            self.redis_dict[user_id] = {'state': self.first_state, 'answers': self.answer_tmpl}

        # если состояние в списке, то просто увеличиваем его на 1
        # ПЛОХО: если номер в базе пропустим, то все упадет
        elif user_state in self.states_list:
            self.redis_dict[user_id]['state'] = self.redis_dict[user_id]['state'] + 1

    def get_question(self, user_id: int):
        """
        Даст нужный вопрос для пользователя.
        State считается от user_id внутри функции.
        Для пользователя всегда будет нужный ему вопрос.
        """

        user_state = self.get_state(user_id)


        # Пользователь начал проходит анкету
        if user_state is None:
            text, descr = '', ''

        # Пользователь проходит анкету
        elif user_state in self.states_list:
            # + 1 потому что во время вопроса у нас состояние на 1 меньше вопроса
            question = NewYearQuestions.get_question_by_number(user_state)
            text = question[2]
            descr = question[3]

        # Пользователь прошел анкету
        else:
            text, descr = '', ''

        return text, descr

    def get_type_question(self, user_id: int):
        number: int | None = self.get_state(user_id)
        if number:
            question = NewYearQuestions.get_question_by_number(number)
            type_question = question[4]

            return type_question
        return None

    def add_text(self, user_id: int, text):
        number: str = str(self.get_state(user_id))
        if number:
            # Создали верхний словарь User_dict
            change_dict = self.redis_dict[user_id]

            # Получили просто словарь body
            answers = change_dict['answers']

            # изменили этот просто словарь
            answers['body'][number]['text_answer'] = answers['body'][number]['text_answer'] + '\n' + text
            # перезаписали user_dict
            change_dict['answers'] = answers

            # ну вышло сложнее, чем я думал

    def add_photo(self, user_id: int, photo_id: str):
        """
        Добавляет фото id в словарь редис
        :param user_id:
        :param text:
        :return:
        """
        number: str = str(self.get_state(user_id))
        if number:
            # Создали верхний словарь User_dict
            change_dict = self.redis_dict[user_id]

            # Получили просто словарь body
            answers = change_dict['answers']

            # изменили этот просто словарь
            answers['body'][number]['photos'].append(photo_id)
            # перезаписали user_dict
            change_dict['answers'] = answers

    def get_all_answers(self, user_id):
        """
        Вернет словарь всех ответов пользователя на все вопросы
        :param user_id: int
        :return: dict
        """
        number: str = str(self.get_state(user_id))
        if number:
            # Создали верхний словарь User_dict
            change_dict = self.redis_dict[user_id]

            # возвращаем dict
            return change_dict.user_dict

    def get_current_button(self, user_id):
        """
        Возвращает текущую кнопку из анкеты, чтобы ее высветить пользователю
        для нажатия
        """
        try:

            user_state = self.get_state(user_id)


            # Пользователь начал проходит анкету
            if user_state is None:
                return 'Отправить'

            # Пользователь проходит анкету
            elif user_state + 1 in self.states_list:
                question = NewYearQuestions.get_question_by_number(user_state + 1)
                button = question[5]
                return button
            else:
                question = NewYearQuestions.get_question_by_number(user_state)
                button = question[5]
                return button
        except Exception as err:
            print(err, str(err), type(err).__name__)
            return 'Отправить'











redis_dict = RedisDict(red)
fsm = FSM(redis_dict)