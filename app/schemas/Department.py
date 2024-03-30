from pydantic import BaseModel
from ..database.config import db
from fastapi import HTTPException
from typing import List


class Department(BaseModel):
    name: str
    manager: str
    employee_ids: List[str]

    class Config:
        json_schema_extra = {
            'collection': 'departments'
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_employees()

    def validate_employees(self):
        employees_collection = db['employees']
        all_employee_ids = {str(employee['_id']) for employee in employees_collection.find({}, {'_id': 1})}
        for employee_id in self.employee_ids:
            if employee_id not in all_employee_ids:
                raise HTTPException(status_code=422, detail=f'Employee with id <{employee_id}> not found')
