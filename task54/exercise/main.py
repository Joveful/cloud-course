from fastapi import FastAPI
from mongoengine import (
    connect,
    disconnect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    IntField,
)
import json
from pydantic import BaseModel

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    # Set the correct parameters to connect to the database
    connect("fast-api-database", host="mongo", port=27017)


@app.on_event("shutdown")
def shutdown_db_client():
    # Set the correct parameters to disconnect from the database
    disconnect("fast-api-database")


# Helper functions to convert MongeEngine documents to json


def course_to_json(course):
    course = json.loads(course.to_json())
    course["students"] = list(map(lambda dbref: str(dbref["$oid"]), course["students"]))
    course["id"] = str(course["_id"]["$oid"])
    course.pop("_id")
    return course


def student_to_json(student):
    student = json.loads(student.to_json())
    student["id"] = str(student["_id"]["$oid"])
    student.pop("_id")
    return student


# Schema


class Student(Document):
    # Implement the Student schema according to the instructions
    name = StringField(required=True)
    student_number = IntField()


class Course(Document):
    # Implement the Course schema according to the instructions
    name = StringField(required=True)
    description = StringField()
    tags = ListField(StringField())
    students = ListField(ReferenceField("Student", reverse_delete_rule=4))


# Input Validators


class CourseData(BaseModel):
    name: str
    description: str | None
    tags: list[str] | None
    students: list[str] | None


class StudentData(BaseModel):
    name: str
    student_number: int | None


# Student routes
# Complete the Student routes similarly as per the instructions provided in A+


@app.post("/students", status_code=201)
def create_student(student: StudentData):
    new_student = Student(**student.dict()).save()
    student_json = student_to_json(new_student)
    return {"message": "Student successfully created", "id": student_json["id"]}


@app.get("/students/{student_id}", status_code=200)
def get_student(student_id: str):
    student = Student.objects.get(id=student_id)
    return student_to_json(student)


@app.put("/students/{student_id}", status_code=200)
def update_student(student_id: str, student: StudentData):
    Student.objects.get(id=student_id).update(**student.dict())
    return {"message": "Student successfully updated"}


@app.delete("/students/{student_id}", status_code=200)
def delete_student(student_id: str):
    Student.objects.get(id=student_id).delete()
    return {"message": "Student successfully deleted"}


# Course routes
# Complete the Course routes similarly as per the instructions provided in A+


@app.post("/courses", status_code=201)
def create_course(course: CourseData):
    new_course = Course(**course.dict()).save()
    course_json = course_to_json(new_course)
    return {"message": "Course successfully created", "id": course_json["id"]}


@app.get("/courses", status_code=200)
def get_courses(tag: str | None = None, studentName: str | None = None):
    if tag and not studentName:
        course = Course.objects.filter(tags=tag)
    elif studentName and not tag:
        student = Student.objects.get(name=studentName)
        course = Course.objects.filter(students=student)
    elif tag and studentName:
        student = Student.objects().get(name=studentName)
        course = Course.objects.filter(tags=tag, students=student)
    else:
        course = Course.objects()
    return json.loads(course.to_json())


@app.get("/courses/{course_id}", status_code=200)
def get_course_by_id(course_id: str):
    course = Course.objects.get(id=course_id)
    return course_to_json(course)


@app.put("/courses/{course_id}", status_code=200)
def update_course(course_id: str, course: CourseData):
    Course.objects.get(id=course_id).update(**course.dict())
    return {"message": "Course successfully updated"}


@app.delete("/courses/{course_id}", status_code=200)
def delete_course(course_id: str):
    Course.objects.get(id=course_id).delete()
    return {"message": "Course successfully deleted"}
