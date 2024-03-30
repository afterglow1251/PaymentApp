from pydantic import BaseModel
from typing import Optional


class Employee(BaseModel):
    name: str
    surname: str
    position: str
    salary: float
    birth_date: Optional[str] = None

    class Config:
        json_schema_extra = {
            'collection': 'employees'
        }
