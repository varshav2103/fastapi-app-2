from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()
class Student(BaseModel):
    name: str
    age: int
    rollno: str 
    department: str

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    rollno: str 
    department: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

# In-memory database for demonstration
students_db = {}

def get_student_logic(id: int):
    if id in students_db:
        return StudentResponse(id=id, **students_db[id].dict())
    return None

def create_student_logic(student: Student):
    new_id = len(students_db) + 1
    students_db[new_id] = student
    return StudentResponse(id=new_id, **student.dict())

def update_student_logic(id: int, student: Student):
    if id in students_db:
        students_db[id] = student
        return StudentResponse(id=id, **student.dict())
    return None

def delete_student_logic(id: int):
    if id in students_db:
        deleted_student = students_db.pop(id)
        return StudentResponse(id=id, **deleted_student.dict())
    return None

@app.post("/student", response_model=StudentResponse)
def create_student_route(student: Student):
    return create_student_logic(student)

@app.get("/student/{id}", response_model=StudentResponse)
def read_student_route(id: int):
    result = get_student_logic(id)
    if result:
        return result
    return {"error": "Student not found"}

@app.put("/student/{id}", response_model=StudentResponse)
def update_student_route(id: int, student: Student):
    result = update_student_logic(id, student)
    if result:
        return result
    return {"error": "Student not found"}

@app.delete("/student/{id}", response_model=StudentResponse)
def delete_student_route(id: int):
    result = delete_student_logic(id)
    if result:
        return result
    return {"error": "Student not found"}

