from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_of_birth = Column(Date)
    start_date = Column(Date)
    position = Column(String)
    level = Column(String)
    salary_level = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
    has_privileges = Column(Boolean)
    coefficients = Column(Integer)

    department = relationship('Department', back_populates='employees')
    ratings = relationship('Rating', back_populates='employee')


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    department_name = Column(String)
    manager = Column(String)
    employee_count = Column(Integer)

    employees = relationship('Employee', back_populates='department')


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    quarter_1 = Column(String)
    quarter_2 = Column(String)
    quarter_3 = Column(String)
    quarter_4 = Column(String)

    employee = relationship('Employee', back_populates='ratings')
