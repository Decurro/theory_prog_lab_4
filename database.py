import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Department, Employee, Rating

load_dotenv()

engine = create_engine(url=(os.getenv('DB_URL')), echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def insert_departments(json_file_path):
    # Чтение данных из json файла
    with open(json_file_path) as file:
        data = json.load(file)

    # Запись данных в таблицу
    for record in data:
        department = Department(department_name=record['department_name'],
                                manager=record['manager'],
                                employee_count=record['employee_count'])
        session.add(department)

    # Сохранение изменений в базе данных
    session.commit()
    session.close()


def insert_employees(json_file_path):
    # Чтение данных из json файла
    with open(json_file_path) as file:
        data = json.load(file)

    # Запись данных в таблицу
    for record in data:
        employee = Employee(full_name=record['full_name'],
                            date_of_birth=datetime.strptime(record['date_of_birth'], '%Y-%m-%d'),
                            start_date=datetime.strptime(record['start_date'], '%Y-%m-%d'),
                            position=record['position'],
                            level=record['level'],
                            salary_level=record['salary_level'],
                            department_id=record['department_id'],
                            has_privileges=record['has_privileges'],
                            )
        session.add(employee)

    # Сохранение изменений в базе данных
    session.commit()
    session.close()


def insert_ratings():
    symbols = 'A', 'B', 'C', 'D', 'E'
    result = session.query(Employee.id).all()
    for i in range(len(result)):
        random_symbols = random.choices(symbols, k=4)
        emp_id = result[i][0]
        rating = Rating(employee_id=emp_id,
                        quarter_1=random_symbols[0],
                        quarter_2=random_symbols[1],
                        quarter_3=random_symbols[2],
                        quarter_4=random_symbols[3])
        session.add(rating)

    # Сохранение изменений в базе данных
    session.commit()
    session.close()


if __name__ == '__main__':
    insert_departments("departments.json")
    insert_employees("employees.json")
    insert_ratings()
