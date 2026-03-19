import sqlite3

conn = sqlite3.connect('computer_builds.db')
cursor = conn.cursor()

cursor.execute('PRAGMA foreign_keys = ON')
cursor.execute('''
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    founded_year INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    manufacturer_id INTEGER,
    category_id INTEGER,
    release_date DATE,
    stock_quantity INTEGER DEFAULT 0,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS builds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    build_date DATE DEFAULT CURRENT_DATE,
    total_price DECIMAL(10, 2),
    purpose VARCHAR(50)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS build_components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    build_id INTEGER NOT NULL,
    component_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (build_id) REFERENCES builds(id) ON DELETE CASCADE,
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
)
''')

print("База данных успешно создана!")

cursor.executemany('''
INSERT INTO manufacturers (name, country, founded_year) VALUES (?, ?, ?)
''', [
    ('Intel', 'США', 1968),
    ('AMD', 'США', 1969),
    ('NVIDIA', 'США', 1993),
    ('Samsung', 'Южная Корея', 1938),
    ('Kingston', 'США', 1987)
])

cursor.executemany('''
INSERT INTO categories (name, description) VALUES (?, ?)
''', [
    ('Процессоры', 'Центральные процессоры для компьютеров'),
    ('Видеокарты', 'Графические ускорители'),
    ('Оперативная память', 'Модули RAM'),
    ('Накопители', 'SSD и HDD диски'),
    ('Материнские платы', 'Системные платы')
])

cursor.executemany('''
INSERT INTO components (name, price, manufacturer_id, category_id, stock_quantity) 
VALUES (?, ?, ?, ?, ?)
''', [
    ('Intel Core i7-12700K', 35000, 1, 1, 10),
    ('AMD Ryzen 7 5800X', 30000, 2, 1, 8),
    ('NVIDIA RTX 3070', 65000, 3, 2, 5),
    ('Samsung 980 Pro 1TB', 15000, 4, 4, 15),
    ('Kingston Fury 32GB', 12000, 5, 3, 12)
])

cursor.executemany('''
INSERT INTO builds (name, total_price, purpose) VALUES (?, ?, ?)
''', [
    ('Игровой ПК', 112000, 'gaming'),
    ('Офисный ПК', 45000, 'office'),
    ('Рабочая станция', 157000, 'workstation')
])

cursor.executemany('''
INSERT INTO build_components (build_id, component_id, quantity) VALUES (?, ?, ?)
''', [(1, 1, 1), (1, 3, 1), (1, 5, 2), (2, 2, 1), (2, 4, 1), (3, 1, 1), (3, 3, 1), (3, 4, 2), (3, 5, 4)
      ])

conn.commit()

conn.close()
print("\nБаза данных закрыта")
