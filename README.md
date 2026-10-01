# Budget Tracker

A learning-focused full-stack project built to practice CRUD, MongoDB, FastAPI, Docker, and CI in a real-world application.

This project is designed for hands-on learning and portfolio work. It demonstrates how to build a small but complete application from the backend to the frontend, with persistent data storage and deployment automation.

## Overview

Budget Tracker is a personal finance dashboard that lets users:

- register and log in
- create income entries
- create expense entries
- view monthly totals and balance
- update and delete expense data
- generate reporting summaries
- export reports as Excel files

It combines a FastAPI backend, a Streamlit frontend, and MongoDB for data persistence.

## Why this project exists

This repository is meant to help learn:

- CRUD development end to end
- MongoDB document-based storage
- FastAPI API design and routing
- JWT authentication
- frontend-backend integration
- Docker container setup
- GitHub Actions CI workflow basics

## Tech Stack

- Python 3.11
- FastAPI
- Streamlit
- MongoDB Atlas
- Motor
- JWT authentication
- Docker + Docker Compose
- GitHub Actions

## Features

- User registration and login
- Secure JWT-based authentication
- Add, list, update, and delete expenses
- Add and view income entries
- Monthly summary and balance calculations
- Report generation by month and year
- Excel report export
- Dockerized setup for local run and CI checks

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── docker-ci.yml
├── backend/
│   └── app/
│       ├── core/
│       │   ├── database.py
│       │   └── security.py
│       ├── models/
│       │   ├── expense_model.py
│       │   ├── income_model.py
│       │   └── user_model.py
│       ├── routes/
│       │   ├── auth.py
│       │   ├── expenses.py
│       │   ├── income.py
│       │   └── reports.py
│       ├── dependencies.py
│       └── main.py
├── frontend/
│   ├── main.py
│   ├── pages/
│   │   └── 1_Dashboard.py
│   └── utils/
│       ├── api_calls.py
│       ├── auth.py
│       └── session.py
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
```

## GitHub workflow

The workflow in [.github/workflows/docker-ci.yml](.github/workflows/docker-ci.yml) is used to validate the project in CI.

It performs a smoke test by:

- checking out the repo
- building the Docker stack
- starting the app
- hitting the backend and frontend endpoints
- shutting the stack down after validation

This helps ensure the project still builds and responds correctly when code is pushed or merged.

## Docker Compose

The Docker Compose setup is used to run the app locally in a simple multi-service setup.

### Services

- backend service for FastAPI
- frontend service for Streamlit
- MongoDB Atlas connection from environment config

## Local run

### 1) Create environment file

Create a root `.env` file with your real Atlas connection string:

```env
MONGO_URL=mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority
DB_NAME=BudgetTracker
API_URL=http://localhost:8000/auth
```

### 2) Install dependencies

```bash
python -m venv .venv
.
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3) Start backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4) Start frontend

```bash
cd frontend
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### 5) Open app

- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

### 6) Docker Compose alternative

```bash
docker compose up --build
```

Then visit:

- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

## End-to-end flow

1. User opens the Streamlit app
2. User registers or logs in
3. Frontend sends requests to the FastAPI backend
4. FastAPI validates the auth flow and returns a JWT
5. User adds expense or income records
6. Records are saved in MongoDB
7. Summary data is read back and displayed in the dashboard
8. Reports can be generated and exported as Excel files

## Important note

This project is intentionally built as a learning project for understanding:

- CRUD patterns
- MongoDB integration
- FastAPI backend architecture
- frontend + API communication
- Docker orchestration
- CI validation basics

It is a clean educational example rather than a production-grade enterprise system.

## License

This project is intended for learning and portfolio use.
