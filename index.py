import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

# Параметры модели
NUM_USERS = 10000
SIM_TIME = 100  # Время симуляции
INTERVAL = 10  # Интервал между запросами TODO: рандомный интервал генерировать

# TODO: добавить intenal server error

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
        yield env.timeout(random.randint(1, INTERVAL))
        env.process(process_request(env, db, request_log))

# Основная функция симуляции
def run_simulation():
    env = simpy.Environment()
    db = simpy.Resource(env, capacity=1)
    request_log = []

    for i in range(NUM_USERS):
        env.process(user(env, db, request_log))

    env.run(until=SIM_TIME)

    return request_log

# Запуск симуляции
request_log = run_simulation()

# Анализ данных
df = pd.DataFrame(request_log, columns=['Time', 'Processing Time'])

# Визуализация результатов
plt.plot(df['Time'], df['Processing Time'])
plt.xlabel('Time')
plt.ylabel('Processing Time')
plt.title('Simulation of Database Requests')
plt.show()