import os
import tempfile
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from .employees import get_all_employees
from ..dependencies.templates import templates
from ..internal.pdf.functions import pdf

router = APIRouter()


@router.get('/home', response_class=HTMLResponse, tags=['home page'])
@router.get('/', response_class=HTMLResponse, tags=['home page'])
async def home(request: Request):
    try:
        employees = await get_all_employees()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred while retrieving employee data: {str(e)}')

    return templates.TemplateResponse('index.html', {'request': request, 'employees': employees})


@router.get('/generate_pdf', tags=['pdf'])
async def generate_pdf():
    try:
        employees = await get_all_employees()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred while retrieving employee data: {str(e)}')

    filename = 'employees'
    pdf(employees, filename=filename)

    return {'message': f'{filename}.pdf'}


@router.get('/file/download', summary='Downloading file', tags=['pdf'])
async def download_file():
    try:
        employees = await get_all_employees()
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            pdf(employees, filename=tmp_file.name)
            return FileResponse(path=f'{tmp_file.name}.pdf', filename='Employees statistics.pdf',
                                media_type='multipart/form-data')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred: {str(e)}')
