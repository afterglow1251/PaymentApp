from app.schemas.Employee import Employee
from typing import List, Callable
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph


def information_paragraph(s: str):
    information_text = '<br/><br/><br/>'.join([s, ""])
    return Paragraph(information_text,
                     ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=14, alignment=1))


def generate_table(employees: List[Employee], title: str, *, key: Callable, reverse: bool = False):
    sorted_employees = sorted(employees, key=key, reverse=reverse)
    employees_dicts = [{pair[0].capitalize(): pair[1] for pair in employee} for employee in sorted_employees]
    df = pd.DataFrame(employees_dicts)
    selected_df = df.drop(columns=['Birth_date'])

    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)])

    table = Table([list(selected_df.columns)] + selected_df.values.tolist())
    table.setStyle(style)

    return information_paragraph(title), table


def pdf(employees: List[Employee], *, filename: str) -> None:
    pdf_filename = f'{filename}.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, topMargin=15)

    elements = [
        *generate_table(employees, 'Sort by name (ascending)', key=lambda employee: employee.name),
        PageBreak(),
        *generate_table(employees, 'Sort by name (descending)', key=lambda employee: employee.name, reverse=True),
        PageBreak(),
        *generate_table(employees, 'Sort by surname (ascending)', key=lambda employee: employee.surname),
        PageBreak(),
        *generate_table(employees, 'Sort by surname (descending)', key=lambda employee: employee.surname, reverse=True),
        PageBreak(),
        *generate_table(employees, 'Sort by position (ascending)', key=lambda employee: employee.position),
        PageBreak(),
        *generate_table(employees, 'Sort by position (descending)', key=lambda employee: employee.position, reverse=True),
        PageBreak(),
        *generate_table(employees, 'Sort by salary (ascending)', key=lambda employee: employee.salary),
        PageBreak(),
        *generate_table(employees, 'Sort by salary (descending)', key=lambda employee: employee.salary, reverse=True)
    ]

    doc.build(elements)

