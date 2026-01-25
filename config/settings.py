
""" Application configuration file.
This file contains all global settings such as project paths, data directory, and application metadata."""
import os
from pathlib import Path

# Base directory of the project
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


