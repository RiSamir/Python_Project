from fastapi import FastAPI
from pydantic import BaseModel
import os
from array import array

app = FastAPI(title="Student & Course Management API (Text File Storage)")

STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"


def load_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [ln.strip() for ln in f.readlines() if ln.strip()]

def write_lines(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines))

def parse_student(line):
    parts = line.split(",", 3)
    return {
        "id": parts[0],
        "name": parts[1],
        "age": int(parts[2]),
        "program": parts[3]
    }

def student_to_line(s):
    return f'{s["id"]},{s["name"]},{s["age"]},{s["program"]}'

def load_students():
    return [parse_student(ln) for ln in load_lines(STUDENTS_FILE)]

def save_students(students):
    write_lines(STUDENTS_FILE, [student_to_line(s) for s in students])


def parse_course(line):
    parts = line.split(",", 3)
    return {
        "course_id": parts[0],
        "title": parts[1],
        "credits": int(parts[2]),
        "student_id": parts[3]
    }

def course_to_line(c):
    return f'{c["course_id"]},{c["title"]},{c["credits"]},{c["student_id"]}'

def load_courses():
    return [parse_course(ln) for ln in load_lines(COURSES_FILE)]

def save_courses(courses):
    write_lines(COURSES_FILE, [course_to_line(c) for c in courses])


class StudentModel(BaseModel):
    id: str
    name: str
    age: int
    program: str

class CourseModel(BaseModel):
    course_id: str
    title: str
    credits: int
    student_id: str



@app.post("/admin/add_student")
def add_student(student: StudentModel):
    students = load_students()
    for s in students:
        if s["id"] == student.id:
            return {"status": "error", "message": "Student ID exists"}
    students.append(student.dict())
    save_students(students)
    return {"status": "success", "message": "Student added"}

@app.get("/admin/list_students")
def list_students():
    return {"students": load_students()}

@app.get("/admin/get_student")
def get_student(id: str):
    for s in load_students():
        if s["id"] == id:
            return {"found": True, "student": s}
    return {"found": False}

@app.put("/admin/update_student")
def update_student(student: StudentModel):
    students = load_students()
    for i, s in enumerate(students):
        if s["id"] == student.id:
            old_data = tuple(s.values())
            students[i] = student.dict()
            save_students(students)
            return {"status": "updated", "old": old_data, "new": students[i]}
    return {"status": "error", "message": "Student not found"}

@app.delete("/admin/delete_student")
def delete_student(id: str):
    students = load_students()

    found = False
    new_students = []

    for s in students:
        if s["id"] == id:
            found = True
        else:
            new_students.append(s)

    if not found:
        return {"status": "error", "message": "Invalid Student ID"}

    save_students(new_students)

    
    courses = load_courses()
    new_courses = [c for c in courses if c["student_id"] != id]
    save_courses(new_courses)

    return {"status": "success", "message": "Student deleted"}


@app.post("/student/add_course")
def add_course(course: CourseModel):
    courses = load_courses()
    for c in courses:
        if c["course_id"] == course.course_id and c["student_id"] == course.student_id:
            return {"status": "error", "message": "Course exists"}
    courses.append(course.dict())
    save_courses(courses)
    return {"status": "success", "message": "Course added"}

@app.get("/student/my_courses")
def my_courses(student_id: str):
    my_list = [c for c in load_courses() if c["student_id"] == student_id]
    return {"courses": my_list}

@app.put("/student/update_course")
def update_course(course: CourseModel):
    courses = load_courses()
    found = False

    for i, c in enumerate(courses):
        if c["course_id"] == course.course_id and c["student_id"] == course.student_id:
            found = True
            courses[i] = course.dict()
            break

    if not found:
        return {"status": "error", "message": "Course not found"}

    save_courses(courses)
    return {"status": "success", "message": "Course updated"}

@app.delete("/student/delete_course")
def delete_course(course_id: str, student_id: str):
    courses = load_courses()
    found = False
    new_list = []

    for c in courses:
        if c["course_id"] == course_id and c["student_id"] == student_id:
            found = True
        else:
            new_list.append(c)

    if not found:
        return {"status": "error", "message": "Invalid course ID"}

    save_courses(new_list)
    return {"status": "success", "message": "Course deleted"}


@app.get("/unique_programs")
def unique_programs():
    students = load_students()
    programs = set(s["program"] for s in students)
    return {"programs": list(programs)}

@app.get("/student_ids_array")
def student_ids_array():
    arr = array('i')
    for s in load_students():
        try:
            arr.append(int(s["id"]))
        except:
            pass
    return {"ids": list(arr)}
