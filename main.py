from datetime import timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID
from sqlmodel import Session, select
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, TokenData, create_access_token, get_current_authority, get_current_student, hash_password, verify_password
from app.db import create_db_and_tables, get_session
from app.models import Authority, AuthorityRegister, Complaint, ComplaintCategory, ComplaintRegister, Student, StudentRegister


app = FastAPI()


@app.on_event("startup")
def startup_event():
    create_db_and_tables()
    
    


@app.get("/")
def root():
    return {"message": "College Complaint Management API is running"}

@app.post("/register/student")
def register_student(data: StudentRegister, session: Session = Depends(get_session)):
    existing = session.exec(select(Student).where(Student.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = Student(
        student_id=data.student_id,
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return {"message": "Student registered successfully"}

@app.post("/register/authority")
def register_authority(data: AuthorityRegister, session: Session = Depends(get_session)):
    existing = session.exec(select(Authority).where(Authority.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    authority = Authority(
        authority_id=data.authority_id,
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    session.add(authority)
    session.commit()
    session.refresh(authority)
    return {"message": "Authority registered successfully"}

@app.post("/login/student")
def login_student(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    student = session.exec(select(Student).where(Student.email == data.username)).first()
    if not student or not verify_password(data.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": student.email, "role": "student"}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login/authority")
def login_authority(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    authority = session.exec(select(Authority).where(Authority.email == data.username)).first()
    if not authority or not verify_password(data.password, authority.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": authority.email, "role": "authority"}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/complaint/create")
def create_complaint(complaint_data: ComplaintRegister, user:TokenData = Depends(get_current_student), session: Session = Depends(get_session)):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can raise complaints")
    
    student = session.exec(select(Student).where(Student.email == user.email)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    complaint = Complaint(
        title=complaint_data.title,
        description=complaint_data.description,
        category=complaint_data.category,
        status=complaint_data.status,
        created_by=student.id
    )
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    return {"message": "Complaint created successfully"}

@app.get("/complaint/view", response_model=List[Complaint])
def view_complaint(category: Optional[ComplaintCategory] = Query(None),
    sort_by_latest: Optional[bool] = Query(False),
    user: TokenData = Depends(get_current_authority),
    session: Session = Depends(get_session)):
    if user.role != "authority":
        raise HTTPException(status_code=403, detail="Only authority can view complaints")
    
    query = select(Complaint).where(Complaint.assigned_to == None)

    if category:
        query = query.where(Complaint.category == category)

    if sort_by_latest:
        query = query.order_by(Complaint.created_at.desc())

    complaints = session.exec(query).all()
    return complaints


@app.post("/complaint/assign/{complaint_id}")
def assign_complaint_to_authority(
    complaint_id: UUID = Path(..., description="ID of the complaint to assign"),
    user: TokenData = Depends(get_current_authority),
    session: Session = Depends(get_session)
):
    if user.role != "authority":
        raise HTTPException(status_code=403, detail="Only authority can assign complaints")

    authority = session.exec(select(Authority).where(Authority.email == user.email)).first()
    if not authority:
        raise HTTPException(status_code=404, detail="Authority not found")

    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint.assigned_to is not None:
        raise HTTPException(status_code=400, detail="Complaint is already assigned")

    complaint.assigned_to = authority.id
    complaint.status = "INPROGRESS"  # or ComplaintStatus.INPROGRESS if using Enum

    session.add(complaint)
    session.commit()
    session.refresh(complaint)

    return {
        "message": "Complaint assigned successfully",
        "complaint_id": complaint.id,
        "assigned_to": authority.name,
        "status": complaint.status
    }

    
    
    

