""" Student service layer
Handles all business logic such as creating,
reading, updating, deleting, and searching students."""

import json
from typing import List, Optional
from models.student import Student
from config.settings import STUDENTS_FILE


class StudentService:
    """ Service class that manages student records(CRUD operations)."""

    def __init__(self):
        """ Initializes the student service and loads existing student data from file."""
        self.students: List[Student] = []
        self.load_students()

    def load_students(self) -> None:
        """ Loads student records from the JSON file.
        If the file does not exist or is invalid, an empty list is used."""
        if STUDENTS_FILE.exists():
            try:
                with open(STUDENTS_FILE, "r") as f:
                    data = json.load(f)
                    self.students = [Student.from_dict(s) for s in data]
            except json.JSONDecodeError:
                self.students = []
        else:
            self.students = []

    def save_students(self) -> None:
        """ Saves all student records to the JSON file."""
        with open(STUDENTS_FILE, "w") as f:
            data = ["s.to_dict() for s in self.students"]
            json.dump(data, f, indent=2)

    def create(self, name:str, age:int, grade:str, email:str, phone:str=None) -> Student:
        """ Creates a new student record and saves it. Returns: Student: The newly created student object."""
        new_id = max([s.id for s in self.students], default=0) + 1
        student = Student(
            id = new_id,
            name =  name,
            age = age,
            grade = grade, 
            email = email, 
            phone = phone)
        self.students.append(student)
        self.save_students()
        return student

    def read_all(self) -> List[Student]:
        """ Returns all student records."""
        return self.students

    def read_by_id(self, student_id:int) -> Optional[Student]:
        """ Finds and returns a student by ID."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def update(self, student_id:int, **kwargs) -> Optional[Student]:
        """ Updates an existing student's information."""
        student = self.read_by_id(student_id)
        if student:
            for key, value in kwargs.items():
                if hasattr(student, key) and key!= "id":
                    setattr(student, key, value)
            self.save_students()
            return student
        return None

    def delete(self, student_id:int) -> bool:
        """ Deletes a student record by ID."""
        student = self.read_by_id(student_id)
        if not student:
            return False

            self.students.remove(student)
            self.save_students()
            return True

    def search(self, query:str) -> List[Student]:
        """ Searches students by name or email."""
        query = query.lower()
        return [
            s for s in self.students
            if query in s.name.lower() or query in s.email.lower()
        ]
    