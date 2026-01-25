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