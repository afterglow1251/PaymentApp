from fastapi import APIRouter, HTTPException
from ..database.config import db
from app.schemas.Department import Department
from bson import ObjectId
from typing import List

router = APIRouter()


@router.get('/department/{department_id}', summary='Get a department by ID', response_model=Department,
            tags=['department'])
async def get_department(department_id: str) -> Department:
    department_data = db['departments'].find_one({'_id': ObjectId(department_id)})
    if department_data:
        return Department(**department_data)
    else:
        raise HTTPException(status_code=404, detail='Department not found')


@router.post('/department', summary='Create a new department', response_model=Department, tags=['department'])
async def create_department(department: Department) -> Department:
    new_department = dict(department)
    db['departments'].insert_one(new_department)
    return department


@router.get('/departments', summary='Get all departments', response_model=List[Department], tags=['departments'])
async def get_all_departments() -> List[Department]:
    departments_data = db['departments'].find()
    return [Department(**department_data) for department_data in departments_data]
