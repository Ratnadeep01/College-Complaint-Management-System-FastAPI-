# 🏫 College Complaint Management System (FastAPI)

This is a backend API system built using **FastAPI** and **SQLModel** for managing complaints raised by students and handled by college authorities. It uses **JWT-based authentication**, with separate login flows for **students** and **authorities**.

---

## 🚀 Features

- 🔒 JWT Authentication (Separate for Student and Authority)
- 📝 Complaint creation (by students)
- 📋 Complaint viewing and assignment (by authorities)
- 🗃️ SQLite database
- 📬 Role-based access control using dependencies

---

## 📦 Tech Stack

- FastAPI
- SQLite (via SQLModel)
- JWT (using `python-jose`)
- Pydantic
- Uvicorn (ASGI server)
- Postman for API testing

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Ratnadeep01/College-Complaint-Management-System-FastAPI-.git
cd college-complaint-management
```
### 2. Create a virtual environment and activate it
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# OR
source .venv/bin/activate  # macOS/Linux
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the server
```bash
uvicorn main:app --reload
```

