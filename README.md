
# 📘 Coursify — Course Planning Platform  
### Fall 2025 — CS 3200 Database Design Project  
### Team Slackers

---

## 🧑‍💻 Team Members
| Name | Role | Northeastern Email |
|------|------|--------------------|
| **Isabella Felix Castillo** | Point Person | felixcastillo.i@northeastern.edu |
| **Neil Keltcher** | Team Member | keltcher.n@northeastern.edu |
| **Camilo Hernandez Macias** | Team Member | hernandezmacias.c@northeastern.edu |
| **Nandhini Natarajan** | Team Member | natarajan.nan@northeastern.edu |
| **Sourya Beesabathuni** | Team Member | beesabathuni.s@northeastern.edu |

---

## 🎯 Project Overview

**Coursify** is a course-planning platform designed to help Northeastern students map out multi-semester degree plans based on requirements, prerequisites, and course demand.

The system supports:
- **Students:** create degree plans using real course data  
- **Professors:** view course demand and section trends  
- **Data Analysts:** aggregate demand for forecasting  
- **System Administrators:** maintain data integrity and database structure

This repository implements:  
✔ Streamlit frontend  
✔ Flask REST API backend  
✔ MySQL database container  
✔ Full SQL schema and sample data  
✔ Reproducible Docker Compose deployment  

---

## Demo Video:
https://drive.google.com/file/d/1UoR1NpyYtnNcqwl8SAqQHLkRH8LTT4o7/view?usp=sharing

---

## 📁 Repository Structure

```
Coursify/
│
├── api/                         # Flask REST API
│   ├── backend/
│   │   ├── db_connection/
│   │   ├── students/
│   │   ├── plans/
│   │   ├── courses/
│   │   ├── professors/
│   │   ├── requirements/
│   │   └── rest_entry.py
│   ├── ml_models/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.template
│
├── app/                         # Streamlit Frontend
│   ├── src/
│   │   ├── modules/
│   │   ├── pages/
│   │   ├── assets/
│   │   └── Home.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── database-files/
│   └── course_planning_db.sql   # Schema + sample data
│
├── datasets/
├── docker-compose.yaml
├── sandbox.yaml
└── README.md
```

---

## 🔐 Environment Setup (.env File)

Before running the application, create a `.env` file in `api/` based on `.env.template`.

### 👉 Your `.env` must contain:

```
SECRET_KEY=someCrazyS3cR3T!Key.!
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=course_planning_db
MYSQL_ROOT_PASSWORD=<any-password>
```

These values must match the Docker Compose configuration exactly.

---

## 🐳 Running the Application With Docker

### ▶️ Start all containers
```
docker compose up -d
```

This launches:
- Streamlit → http://localhost:8501  
- Flask API → http://localhost:4000  
- MySQL DB → internal hostname: `db`  

### ⛔ Stop everything
```
docker compose down
```

### 🔁 Restart a specific service
```
docker compose restart api
```

### 🗑 Rebuild database after SQL changes
```
docker compose down db -v
docker compose up db -d
```

This wipes the old MySQL volume and reloads the `.sql` file.

---

## 🌐 Service URLs

| Service | URL |
|--------|-----|
| **Frontend (Streamlit)** | http://localhost:8501 |
| **Backend API (Flask)** | http://localhost:4000 |
| **MySQL (host)** | localhost:3306 |
| **MySQL (in Docker network)** | db:3306 |

---

## 🔗 API Routes (Blueprint Prefixes)

The following prefix mappings come from `rest_entry.py`:

| Component | Prefix | Example |
|----------|--------|---------|
| Students | `/s` | `/s/student1001/plans` |
| Plans | `/p` | `/p/plans/1/courses` |
| Courses | `/c` | `/c/courses?subject=CS` |
| Professors | `/prof` | `/prof/professors/1001/sections` |
| Requirements | `/r` | `/r/requirements/...` |
| Data | `/d` | `/d/data/...` |

---

## 🏠 Streamlit Home (Role-Based Mock Login)

The homepage (`Home.py`) lets users choose a persona:

- **Andrea — Student**  
- **Amelia — Professor**  
- **System Administrator**  
- **Data Analyst**

Selecting a persona stores role data in `st.session_state` and loads the appropriate pages.

This simulates RBAC without real authentication.

---

## 🧱 Database Notes

- MySQL executes all `.sql` files in `database-files/` **in alphabetical order**  
- The main schema + inserts file is:  
  **`course_planning_db.sql`**

To reload SQL:
```
docker compose down db -v
docker compose up db -d
```

---

## 🧪 Development Tips

- Streamlit & API reload automatically when code changes  
- If Streamlit isn’t updating, click **Always rerun**  
- If the API crashes due to a Python error, fix the code and run:

```
docker compose restart api
```

---


This repository includes:

✔ ER-to-Relational schema implemented in SQL  
✔ All metadata & foreign keys  
✔ Full REST API for all entities
✔ Working Streamlit UI pages
✔ Role-based UX behavior
✔ 3-tier system deployment (Frontend → API → MySQL)
✔ Fully reproducible Docker setup
✔ Clear setup documentation

---

## 📄 License
For educational use in **CS 3200 — Database Design**, Northeastern University.
