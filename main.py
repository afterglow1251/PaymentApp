from fastapi import FastAPI

from app.routers import employees, departments, main

app = FastAPI()

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(main.router)
