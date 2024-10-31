import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

# Параметры модели
# NUM_USERS = 10000
SIM_TIME = 100  # Время симуляции
INTERVAL = 50  # Интервал между запросами 

# TODO: добавить intenal server error - DONE
# TODO: генерировать количество пользователей - DONE
# TODO: придумать адекватное отображение ошибки при internal server error, например строит график с пользователями
#       а потом начинается перегруз сервака и появляется ошибка, пока такое себе

# Функция срабатывания отказа сервака
def server_error():
    error = False # Переменная - флаг, указывающая наличие ошибки, по умолчанию False
    max_connection = 45000 # Пока пусть число максимальных подключений будет захаркожено
    current_connection = generate_users()
    
    if current_connection > max_connection:
        error = True
        
    return error

# Функция генерации рандомного количества пользователей
def generate_users():
    num_users = random.randint(1, 50000) # Рандомно генерим количество юзеров, далее будем смотреть на это число
                                         # для симуляции падения сервака
    return num_users

# Функция для обработки запроса
def process_request(env, db, request_log):
    with db.request() as request:
        yield request
        processing_time = random.randint(1, 5)
        yield env.timeout(processing_time)  # Время обработки запроса
        request_log.append((env.now, processing_time))

# Функция для генерации запросов
def user(env, db, request_log):
    while True:
        yield env.timeout(random.randint(1, INTERVAL)) # тут уже интервал генерится рандомно, 
                                                       # поэтому отдельную функцию я решил не делать
        env.process(process_request(env, db, request_log))

# Основная функция симуляции
def run_simulation():
    env = simpy.Environment()
    db = simpy.Resource(env, capacity=1)
    request_log = []
    num_users = generate_users() # Здесь вызываем функцию генерации количества пользователей

    for i in range(num_users):
        env.process(user(env, db, request_log))

    env.run(until=SIM_TIME)

    return request_log

# Анализ данных и запуск симуляции
def start_simulation():
    error = server_error()

    if error == True:
        plt.text(0.5, 0.5, 'Server Error', horizontalalignment='center', verticalalignment='center', fontsize=20, color='red')
        plt.axis('off')
        plt.title('Simulation of Database Requests')
        plt.show()
    else:
        df = pd.DataFrame(run_simulation(), columns=['Time', 'Processing Time'])
        # Визуализация результатов
        plt.plot(df['Time'], df['Processing Time'])
        plt.xlabel('Time')
        plt.ylabel('Processing Time')
        plt.title('Simulation of Database Requests')
        plt.show()


start_simulation()