import time
import random
import psycopg2
from threading import Thread

# Функция для подключения к базе данных
def get_db_connection():
    return psycopg2.connect(
        host="db",         # имя контейнера с базой данных
        database="tourismdb",
        user="postgres",
        password="password"
    )

# Функция для обновления километража случайным образом
def update_mileage():
    while True:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Получаем все машины из базы данных
            cur.execute("SELECT id, mileage FROM cars")
            cars = cur.fetchall()

            for car in cars:
                car_id, current_mileage = car
                # Увеличиваем километраж случайным образом от 1 до 5 км
                increment = random.randint(1, 5)
                new_mileage = current_mileage + increment

                # Обновляем километраж в базе данных
                cur.execute("UPDATE cars SET mileage = %s WHERE id = %s", (new_mileage, car_id))

            conn.commit()
            cur.close()
            conn.close()

            print(f"Mileage updated successfully. Incremented by {increment} km.")
        except Exception as e:
            print(f"Error: {e}")

        # Пауза на 2 секунды, чтобы имитировать периодическое обновление
        time.sleep(2)

# Запуск потока для обновления километража
if __name__ == "__main__":
    thread = Thread(target=update_mileage)
    thread.daemon = True
    thread.start()

    # Ожидаем завершения потока
    while True:
        time.sleep(1)
