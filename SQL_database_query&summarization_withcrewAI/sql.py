import sqlite3
from faker import Faker

def create_table():
    """Create Employee table"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employee (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      dept TEXT,
                      salary REAL)''')
    conn.commit()
    conn.close()

def insert_employee(id, name, dept, salary):
    """Insert a new employee into the Employee table"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employee (id, name, dept, salary) VALUES (?, ?, ?, ?)", (id, name, dept, salary))
    conn.commit()
    conn.close()

def generate_fake_data(num_records):
    """Generate fake data using faker"""
    fake = Faker()
    for i in range(1, num_records + 1):
        name = fake.name()
        dept = fake.job()
        salary = fake.random_number(digits=5)
        insert_employee(i, name, dept, salary)

# Create the Employee table if it doesn't exist
create_table()

# Generate and insert fake data
generate_fake_data(100)
