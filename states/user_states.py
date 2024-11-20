from aiogram.fsm.state import default_state, State, StatesGroup
from database.methods import NewYearQuestions
import redis
import json

red = redis.Redis(host='localhost', port=6379, db=0)

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
        self.create_answer_tmpl()  # создаем шаблон ответа

    def update_states(self):
        """
        Получаем состояния из БД. Состояния это номера вопросов
        """
        self.states_list = sorted(NewYearQuestions.get_active_question_numbers())
        self.first_state = self.states_list[0]
        self.last_state = self.states_list[-1] + 1 # последнее состояние - вопросы пройдены

    def create_answer_tmpl(self):
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

    def get_state(self, user_id: int):
        state = self.redis_dict[user_id]
        if state is None:
            return None
        else:
            return self.redis_dict[user_id]['state']

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
            self.next_state(user_id)
            user_state = self.get_state(user_id)
            question = NewYearQuestions.get_question_by_number(user_state)

        # Пользователь проходит анкету
        elif user_state in self.states_list:
            question = NewYearQuestions.get_question_by_number(user_state)

        # Пользователь прошел анкету
        else:
            question = None

        return question








redis_dict = RedisDict(red)
fsm = FSM(redis_dict)
print(fsm.get_state(32))
print(fsm.get_question(56))
fsm.next_state(32)
print(fsm.get_state(32))
print(fsm.get_question(32))
fsm.next_state(32)
print(fsm.get_state(32))
print(fsm.get_question(32))