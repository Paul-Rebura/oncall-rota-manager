# On-Call Rota Manager

A command-line application built in Python to manage on-call schedules, engineer details, and incident logging.

---

## Project Overview

This tool was inspired by real on-call management workflows used within a managed services environment. The application allows teams to manage engineer rotas, assign on-call shifts across date ranges, and log incidents that occur during those shifts, all from the terminal.

The project demonstrates:
- A working CLI application with a structured menu system
- Full CRUD operations against a SQLite database
- Linked data across three related tables
- Input validation and error handling throughout
- A test suite written using pytest
- A CI pipeline via GitHub Actions that runs tests on every push

---

## Project Structure

```
oncall-rota-manager/
├── app/
│   ├── init.py
│   ├── database.py       
│   ├── engineers.py     
│   ├── rota.py           
│   ├── incidents.py      
│   └── menu.py          
├── tests/
│   ├── init.py
│   ├── test_engineers.py
│   ├── test_rota.py
│   └── test_incidents.py
├── .github/
│   └── workflows/
│       └── ci.yml       
├── main.py              
├── requirements.txt
└── README.md
```
---

## Features

### Engineer Management
- Add engineers with name, email, and optional phone number
- View all engineers sorted alphabetically
- Search engineers by name
- Update engineer details (keeps existing values if left blank)
- Delete engineers with confirmation prompt

### Rota Management
- Assign engineers to on-call slots with a start and end date
- View the full rota sorted by start date
- Query who is on-call for any given date (date range aware)
- View all rota entries for a specific engineer
- Delete rota entries with confirmation prompt

### Incident Management
- Log incidents against an active rota entry
- Set severity levels: `low`, `medium`, `high`, `critical`
- View all incidents with engineer and rota context
- Filter incidents by severity
- Sort incidents by severity using a bubble sort algorithm (critical → low)
- Mark incidents as resolved

---

## Getting Started

### Prerequisites
- Python 3.12+
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/oncall-rota-manager.git
cd oncall-rota-manager
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

The database (`oncall_rota.db`) will be created automatically on first run.

---

## Running the Tests

```bash
pytest tests/ -v
```

Tests use isolated temporary databases so they never affect your real data. The test suite covers:
- Adding, retrieving, updating, and deleting engineers
- Assigning rota entries and querying by date range
- Logging incidents, filtering by severity, resolving, and sorting

---

## CI Pipeline

Every push to `dev` or `main`, and every pull request into `main`, triggers the GitHub Actions workflow which:

1. Checks out the code
2. Sets up Python 3.12
3. Installs dependencies from `requirements.txt`
4. Runs the full pytest suite

The workflow file is located at `.github/workflows/test-pipeline.yml`.

---

## Database Schema

### Engineers
| Column | Type    | Notes              |
|--------|---------|--------------------|
| id     | INTEGER | Primary key        |
| name   | TEXT    | Required           |
| email  | TEXT    | Required, unique   |
| phone  | TEXT    | Optional           |

### Rota
| Column      | Type    | Notes                        |
|-------------|---------|------------------------------|
| id          | INTEGER | Primary key                  |
| engineer_id | INTEGER | Foreign key → engineers.id   |
| start_date  | TEXT    | YYYY-MM-DD format            |
| end_date    | TEXT    | YYYY-MM-DD format            |
| shift       | TEXT    | 'day' or 'night'             |

### Incidents
| Column      | Type    | Notes                          |
|-------------|---------|--------------------------------|
| id          | INTEGER | Primary key                    |
| rota_id     | INTEGER | Foreign key → rota.id          |
| title       | TEXT    | Required                       |
| severity    | TEXT    | low / medium / high / critical |
| description | TEXT    | Optional                       |
| raised_at   | TEXT    | Auto-set on creation           |
| resolved    | INTEGER | 0 = open, 1 = resolved         |

---

## Branching Strategy

| Branch | Purpose                              |
|--------|--------------------------------------|
| main   | Stable, production-ready code only   |
| dev    | Active development branch            |

All development work is done on `dev` and merged into `main` via a pull request once stable and all tests are passing.

---

## Technologies Used

| Tool           | Purpose                        |
|----------------|--------------------------------|
| Python 3.12    | Application language           |
| SQLite3        | Lightweight relational database|
| pytest         | Testing framework              |
| GitHub Actions | CI pipeline                    |
| Git            | Version control                |