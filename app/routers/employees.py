from fastapi import APIRouter, HTTPException
from ..database.config import db
from app.schemas.Employee import Employee
from bson import ObjectId
from typing import List

router = APIRouter()


@router.get('/employee/{employee_id}', summary='Get an employee by ID', response_model=Employee, tags=['employee'])
async def get_employee(employee_id: str) -> Employee:
    employee_data = db['employees'].find_one({'_id': ObjectId(employee_id)})
    if employee_data:
        return Employee(**employee_data)
    else:
        raise HTTPException(status_code=404, detail='Employee not found')


@router.post('/employee', summary='Create a new employee', response_model=Employee, tags=['employee'])
async def create_employee(employee: Employee) -> Employee:
    new_employee = dict(employee)
    db['employees'].insert_one(new_employee)
    return employee


@router.get('/employees', summary='Get all employees', response_model=List[Employee], tags=['employees'])
async def get_all_employees() -> List[Employee]:
    employees_data = db['employees'].find()
    return [Employee(**employee_data) for employee_data in employees_data]


@router.post('/employees', summary='Create new employees', response_model=Employee, tags=['employees'])
async def create_employee(employees: List[Employee]) -> List[Employee]:
    new_employees = [employee.dict() for employee in employees]
    db['employees'].insert_many(new_employees)
    return employees
