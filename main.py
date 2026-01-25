
""" Main application file.
# Provides a command-line interface (CLI)
# for interacting with the Student Management System. """

import os
from services.student_service import StudentService
from config.settings import APP_NAME, APP_VERSION

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_header():
    """Print application header"""
    print("=" * 60)
    print(f"  {APP_NAME} v{APP_VERSION}".center(60))
    print("=" * 60)

def print_menu():
    """Print main menu"""
    print("\n📚 Main Menu:")
    print("  1. ➕ Add New Student")
    print("  2. 📋 View All Students")
    print("  3. 🔍 Search Student")
    print("  4. ✏️  Update Student")
    print("  5. ❌ Delete Student")
    print("  6. 🚪 Exit")
    print("-" * 60)


def display_student(student):
    """Display single student details"""
    print(f"\n{'─' * 60}")
    print(f"  ID:         {student.id}")
    print(f"  Name:       {student.name}")
    print(f"  Age:        {student.age}")
    print(f"  Grade:      {student.grade}")
    print(f"  Email:      {student.email}")
    print(f"  Phone:      {student.phone or 'N/A'}")
    print(f"  Created:    {student.created_at}")
    print(f"{'─' * 60}")


def display_students_table(students):
    """Display students in table format"""
    if not students:
        print("\n❌ No students found!")
        return
    print(f"\n{'=' * 100}")
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<30} {'Phone':<15}")
    print(f"{'=' * 100}")

    for s in students:
        print(f"{s.id:<5} {s.name:<20} {s.age:<5} {s.grade:<10} {s.email:<30} {s.phone or 'N/A':<15}")

    print(f"{'=' * 100}")
    print(f"Total Students: {len(students)}")


def add_student(service):
    """Add new student"""
    print("\n➕ Add New Student")
    print("-" * 60)

    try:
        name = input("  Name: ").strip()
        age = int(input("  Age: ").strip())
        grade = input("  Grade: ").strip()
        email = input("  Email: ").strip()     
        phone = input("  Phone (optional): ").strip() or None

        student = service.create(name, age, grade, email, phone)
        print(f"\n✅ Student added successfully! ID: {student.id}")

    except ValueError:
        print("\n❌ Invalid input! Please enter correct data.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def view_all_students(service):
    """View all students"""
    print("\n📋 All Students")
    print("-" * 60)
    students = service.read_all()
    display_students_table(students)


def search_student(service):
    """Search for student"""
    print("\n🔍 Search Student")
    print("-" * 60)
    query = input("  Enter name or email: ").strip()

    if not query:
        print("\n❌ Search query cannot be empty!")
        return

    students = service.search(query)
    display_students_table(students)


def update_student(service):
    """Update student information"""
    print("\n✏️  Update Student")
    print("-" * 60)

    try:
        student_id = int(input("  Enter Student ID: ").strip())
        student = service.read_by_id(student_id)

        if not student:
            print(f"\n❌ Student with ID {student_id} not found!")
            return

        print("\n  Current Details:")
        display_student(student)

        print("\n  Enter new values (press Enter to skip):")
        name = input(f"  Name [{student.name}]: ").strip()
        age = input(f"  Age [{student.age}]: ").strip()
        grade = input(f"  Grade [{student.grade}]: ").strip()
        email = input(f"  Email [{student.email}]: ").strip()
        phone = input(f"  Phone [{student.phone or 'N/A'}]: ").strip()

        updates = {}
        if name: updates['name'] = name
        if age: updates['age'] = int(age)
        if grade: updates['grade'] = grade
        if email: updates['email'] = email
        if phone: updates['phone'] = phone

        if updates:
            service.update(student_id, **updates)
            print("\n✅ Student updated successfully!")
        else:
            print("\n⚠️  No changes made.")

    except ValueError:
        print("\n❌ Invalid input!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def delete_student(service):
    """Delete student"""
    print("\n❌ Delete Student")
    print("-" * 60)

    try:
        student_id = int(input("  Enter Student ID: ").strip())
        student = service.read_by_id(student_id)

        if not student:
            print(f"\n❌ Student with ID {student_id} not found!")
            return

        display_student(student)
        confirm = input("\n  Are you sure you want to delete? (yes/no): ").strip().lower()

        if confirm == 'yes':
            service.delete(student_id)
            print("\n✅ Student deleted successfully!")
        else:
            print("\n⚠️  Deletion cancelled.")

    except ValueError:
        print("\n❌ Invalid input!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Main application loop"""
    service = StudentService()

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("  Enter your choice (1-6): ").strip()

        if choice == '1':
            add_student(service)
        elif choice == '2':
            view_all_students(service)
        elif choice == '3':
            search_student(service)
        elif choice == '4':
            update_student(service)
        elif choice == '5':
            delete_student(service)
        elif choice == '6':
            print("\n👋 Thank you for using Student Management System!")
            print("   Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice! Please select 1-6.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()