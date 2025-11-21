import sqlite3
from datetime import datetime, timedelta
import random

# Имя файла базы данных
DB_NAME = "db.sqlite"

# Подключение к БД (создаёт файл, если не существует)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 1. Таблица users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        registration_date DATE
    )
''')

# 2. Таблица departments
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT
    )
''')

# 3. Таблица employees
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department_id INTEGER,
        salary REAL,
        hire_date DATE,
        FOREIGN KEY (department_id) REFERENCES departments (id)
    )
''')

# 4. Таблица products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL,
        category TEXT
    )
''')

# 5. Таблица orders
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date DATE,
        total REAL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')

# Тестовые данные
names = ["Иван Иванов", "Мария Смирнова", "Алексей Попов", "Елена Кузнецова", "Дмитрий Волков", "Ольга Морозова", "Андрей Новиков", "Татьяна Лебедева", "Сергей Зайцев", "Наталья Власова"]
emails = [f"user{i}@example.com" for i in range(1, 11)]
departments = [("IT", "Москва"), ("Продажи", "СПб"), ("HR", "ЕКб"), ("Финансы", "НН"), ("Маркетинг", "Казань")]
products = [
    ("Ноутбук", 50000.0, "Электроника"),
    ("Мышь", 1000.0, "Электроника"),
    ("Клавиатура", 2500.0, "Электроника"),
    ("Стул", 8000.0, "Мебель"),
    ("Стол", 15000.0, "Мебель"),
    ("Книга", 500.0, "Книги"),
    ("Телефон", 30000.0, "Электроника"),
    ("Планшет", 25000.0, "Электроника"),
    ("Чайник", 3000.0, "Бытовая техника"),
    ("Тостер", 2000.0, "Бытовая техника")
]

# Вставка данных в users
for i in range(10):
    name = names[i]
    email = emails[i]
    age = random.randint(20, 60)
    reg_date = (datetime.now() - timedelta(days=random.randint(1, 365*3))).strftime('%Y-%m-%d')
    cursor.execute("INSERT OR IGNORE INTO users (name, email, age, registration_date) VALUES (?, ?, ?, ?)",
                   (name, email, age, reg_date))

# Вставка данных в departments
for dept in departments:
    cursor.execute("INSERT OR IGNORE INTO departments (name, location) VALUES (?, ?)", dept)

# Вставка данных в products
for prod in products:
    cursor.execute("INSERT OR IGNORE INTO products (name, price, category) VALUES (?, ?, ?)", prod)

# Вставка данных в employees
for i in range(15):
    name = f"Сотрудник {i+1}"
    dept_id = random.randint(1, len(departments))
    salary = round(random.uniform(30000, 150000), 2)
    hire_date = (datetime.now() - timedelta(days=random.randint(1, 365*5))).strftime('%Y-%m-%d')
    cursor.execute("INSERT OR IGNORE INTO employees (name, department_id, salary, hire_date) VALUES (?, ?, ?, ?)",
                   (name, dept_id, salary, hire_date))

# Вставка данных в orders
for i in range(30):
    user_id = random.randint(1, 10)
    product_id = random.randint(1, len(products))
    quantity = random.randint(1, 5)
    order_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    total = round(products[product_id - 1][1] * quantity, 2)
    cursor.execute("INSERT OR IGNORE INTO orders (user_id, product_id, quantity, order_date, total) VALUES (?, ?, ?, ?, ?)",
                   (user_id, product_id, quantity, order_date, total))

# Сохранение изменений и закрытие
conn.commit()
conn.close()

print(f"База данных '{DB_NAME}' успешно создана и заполнена тестовыми данными.")