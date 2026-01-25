1. 📚 Student Management System  (Python CLI)
2. A simple **Python command-line application** to manage student records.
3. 
 
This project is beginner-friendly and demonstrates basic Python concepts
like file handling, classes, and CRUD operations.
This project is built to understand **real-world Python project structure**.

---

2. 🔍 Project Overview

The Student Management System helps users:

- Store student information
- Update and delete records
- Search students easily
- Save data permanently using a JSON file

This project focuses on **clean code, modular design, and file handling**.

---

3. ✨ Features

- ➕ Add new students
- 📋 View all students
- 🔍 Search students by name or email
- ✏️ Update student details
- ❌ Delete student records
- 💾 Persistent storage using JSON

---

4. 🧠 Skills Demonstrated

- Python programming and Python Dataclasses (Modern data structures)
- Object-Oriented Programming (OOP)
- CRUD operations (Create, Read, Update, Delete)
- File handling with JSON (Reading/writing JSON )
- Project structuring (models, services, config)
- Command-line interface(CLI) Development (Building terminal applications ) 
- Git & GitHub workflow

---

5. 🛠️ Technologies Used

- Python 3
- JSON (data storage)
- VS Code
- Git & GitHub

---

6. 📂 Project Structure

student_management/         # Create project folder
├── config/
   └── settings.py          # Application settings
   └── __init__.py          # Create empty __
├── models/
   └── student.py           # Student data model
   └── __init__.py
├── services/   
   └──  student_service.py  # Business logic (CRUD operations)
   └── __init__.py
└── main.py                 # Entry point of your project
└── README.md               # Project documentation
├── data/                   #(auto created)
   └──students.json         # Stored student records(auto created)

---

7. 💻️ Complete Code 

 7.1. 📄 config/settings.py


""" Application configuration file.
This file contains all global settings such as project paths, data directory, and application metadata."""

import os
from pathlib import Path

# Base direcory of your project
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory to store application data
DATA_DIR = BASE_DIR / "data"

# Create data directory if it does not exist
DATA_DIR.mkdir(exist_ok=True)

# Database file (Path to JSON file that stores student records)
STUDENTS_FILE = DATA_DIR / "students.json"

# Application information
APP_NAME = "Student Management System"
APP_VERSION = "1.0.0"


7.2  📄 models/student.py


from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Student:
    """Student data model"""
    id: int
    name: str
    age: int
    grade: str
    email: str
    phone: Optional[str] = None
    created_at: str = None

    def __post_init__(self):
        """Auto-generate timestamp if not provided"""
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Convert student to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """Create student from dictionary"""
        return cls(**data)

    def __str__(self) -> str:
        """String representation"""
        return f"Student(ID: {self.id}, Name: {self.name}, Grade: {self.grade})"


7.3. 📄 services/student_service.py


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
    

7.4. 📄 main.py


""" Main application file.
Provides a command-line interface (CLI)
for interacting with the Student Management System. """

import os
from services.student_service import StudentService
from config.settings import APP_NAME, APP_VERSION


def clear_screen():
    """ Clears the terminal screen. """
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """ Displays application header. """
    print("=" * 50)
    print(f"{APP_NAME} v{APP_VERSION}".center(50))
    print("=" * 50)


def print_menu():
    """ Displays main menu options. """
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")


def main():
    """ Main program loop.
    Handles user interaction and menu navigation. """
    service = StudentService()

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("Choose (1-6): ")

        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            grade = input("Grade: ")
            email = input("Email: ")
            service.create(name, age, grade, email)
            input("Student added. Press Enter...")

        elif choice == "2":
            for student in service.read_all():
                print(student)
            input("Press Enter...")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            input("Invalid choice. Press Enter...")


if __name__ == "__main__":
    main()


8. ▶️ How to Run the Project

8.1. Clone the repository

```bash
git clone https://github.com/Priti-codehub/student-management-system.git
```

8.2. Run the Application

```bash
cd student_management
python main.py
```

8.3 Sample Data
 
Try adding these students:
 
**Student 1:**
- Name: Lee Min Ho
- Age: 38
- Grade: A
- Email: minho@email.com
- Phone: 9876543210
 
**Student 2:**
- Name: Xu Kai
- Age: 30
- Grade: B
- Email: soso@email.com
- Phone: 1234567890


🎉 Congratulations!
 
You've completed a full Python application with:
- ✅ Professional structure
- ✅ CRUD operations
- ✅ File persistence
- ✅ Error handling
- ✅ Beautiful CLI
 
**Keep coding! 🚀**
 
