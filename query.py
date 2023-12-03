from models import Employee, Department, Rating
from database import session
from sqlalchemy import func


# Запросы для получения информации
# 6.1 Уникальный номер сотрудника, его ФИО и стаж работы – для всех сотрудников компании
def get_all_employees():
    all_employees = session.query(Employee).all()
    for employee in all_employees:
        print(employee.id, employee.full_name, employee.start_date)


# 6.2 Уникальный номер сотрудника, его ФИО и стаж работы – только первых 3-х сотрудников
def get_first_3_employees():
    first_three_employees = session.query(Employee).limit(3).all()
    for employee in first_three_employees:
        print(employee.id, employee.full_name, employee.start_date)


# 6.3 Уникальный номер сотрудников - водителей
def get_employees_drivers():
    driver_employees = session.query(Employee).filterby(position='Driver').all()
    for employee in driver_employees:
        print(employee.id)


# 6.4 Выведите номера сотрудников, которые хотя бы за 1 квартал получили оценку D или E
def get_employees_D_E():
    employees_with_low_evaluations = session.query(Employee).join(Rating).filter(
        (Rating.quarter_1.in_(["D", "E"])) |
        (Rating.quarter_2.in_(["D", "E"])) |
        (Rating.quarter_3.in_(["D", "E"])) |
        (Rating.quarter_4.in_(["D", "E"]))
    ).all()

    for employee in employees_with_low_evaluations:
        print(employee.id)


# 6.5 Выведите самую высокую зарплату в компании.
def get_high_salary_in_company():
    highest_salary = session.query(Employee).order_by(Employee.salary_level.desc()).first()
    print(highest_salary.salary_level)


# 6.6 * Выведите название самого крупного отдела
def get_largest_department():
    largest_department = session.query(Department).order_by(Department.employee_count.desc()).first()
    print(largest_department.department_name, largest_department.employee_count)


# 6.7 * Выведите номера сотрудников от самых опытных до вновь прибывших
def get_exp_employees():
    experience_employees = session.query(Employee).order_by(Employee.start_date.asc()).all()
    for employee in experience_employees:
        print(employee.id)


# 6.8 * Рассчитайте среднюю зарплату для каждого уровня сотрудников
def get_avg_salaries():
    salary_by_level = session.query(Employee.salary_level, func.avg(Employee.salary_level)).group_by(
        Employee.salary_level).all()
    for level, avg_salary in salary_by_level:
        print(level, avg_salary)


# 6.9 Добавьте столбец с информацией о коэффициенте годовой премии к основной таблице. Коэффициент рассчитывается по
# такой схеме: базовое значение коэффициента – 1, каждая оценка действует на коэффициент так:
# • Е – минус 20%
# • D – минус 10%
# • С – без изменений
# • B – плюс 10%
# • A – плюс 20%
# Соответственно, сотрудник с оценками А, В, С, D – должен получить коэффициент 1.2.

def calculate_coefficient(assessment):
    if assessment == 'A':
        return 0.2
    elif assessment == 'B':
        return 0.1
    elif assessment == 'D':
        return 0.9
    elif assessment == 'E':
        return 0.8
    elif assessment == '':
        return 0
    else:
        return 1.0


def get_coefficients_employees():
    employees = session.query(Rating).all()
    result = session.query(Employee.id).all()

    for employee in employees:
        assessments = [employee.quarter_1, employee.quarter_2, employee.quarter_3, employee.quarter_4]
        coefficients = [calculate_coefficient(assessment) for assessment in assessments]
        annual_coefficient = 1 + sum(coefficients)
        b = session.query(Employee).filter(Employee.id == employee.employee_id).first()
        b.coefficients = annual_coefficient
    session.commit()


if __name__ == '__main__':
    # pass
    # get_all_employees()
    # get_first_3_employees()
    # get_employees_D_E()
    # get_high_salary_in_company()
    # get_largest_department()
    # get_exp_employees()
    # get_avg_salaries()
    get_coefficients_employees()
