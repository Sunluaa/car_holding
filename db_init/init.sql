-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL
);

-- Создание таблицы автомобилей с полем километража
CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    color VARCHAR(50),
    year INTEGER,
    make VARCHAR(100),
    license_plate VARCHAR(20),
    mileage INTEGER DEFAULT 0
);

-- Вставка данных
INSERT INTO users (username, password) VALUES ('admin', 'admin');
INSERT INTO users (username, password) VALUES ('admin123', '123');
INSERT INTO users (username, password) VALUES ('123', '123');
INSERT INTO cars (color, year, make, license_plate) VALUES ('red', 2005, 'gtr', 'x205oa 777');
INSERT INTO cars (color, year, make, license_plate) VALUES ('black', 2014, 'Qashqai', 'a123bc 77');
INSERT INTO cars (color, year, make, license_plate) VALUES ('green', 2022, 'X-Trail', 'с456ур 99');
INSERT INTO cars (color, year, make, license_plate) VALUES ('green', 2000, 'Leaf', ' с789но 50');
