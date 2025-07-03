from datetime import date, datetime
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from pydantic import EmailStr
from enum import Enum

class ComplaintCategory(str, Enum):
    ACADEMIC = "ACADEMIC"
    HOSTEL = "HOSTEL"
    MESS = "MESS"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    LIBRARY = "LIBRARY"
    CANTEEN = "CANTEEN"
    
class ComplaintStatus(str, Enum):
    PENDING = "PENDING"
    INPROGRESS = "IN-PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"

class Student(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: str = Field(unique=True, index=True)
    name: str
    email: EmailStr = Field(unique=True, index=True)
    password_hash: str

class Authority(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    authority_id: str = Field(unique=True, index=True)
    name: str
    email: EmailStr = Field(unique=True, index=True)
    password_hash: str
    
class Complaint(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=100)
    description: str
    category: ComplaintCategory = Field(
        nullable=False
    )
    status: ComplaintStatus = Field(
        default=ComplaintStatus.PENDING,
        nullable=False
    )
    created_by: uuid.UUID = Field(
        nullable=False,
        foreign_key="student.id",
    )
    assigned_to: Optional[uuid.UUID] = Field(default=None, foreign_key="authority.id")
    deadline: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    

class StudentRegister(SQLModel):
    student_id: str
    name: str
    email: EmailStr
    password: str

class AuthorityRegister(SQLModel):
    authority_id: str
    name: str
    email: EmailStr
    password: str

    
class ComplaintRegister(SQLModel):
    title: str
    description: str
    category: ComplaintCategory
    status: ComplaintStatus = Field(default=ComplaintStatus.PENDING)
    

    

