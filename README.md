# Muuse Tayo Hiring System

Enterprise recruitment platform for Muuse Tayo Construction Company.

## Requirements

- Python 3.10+
- SQLite (default) or Oracle Database Enterprise Edition

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Copy environment file and adjust as needed:

```bash
copy .env.example .env
```

Run migrations and seed sample data:

```bash
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open http://127.0.0.1:8000/users/login/

### Default Accounts (after seed)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | System Administrator |
| hr_manager | hr123 | HR Manager |
| recruiter | rec123 | Technical Recruiter |
| interviewer | int123 | Interviewer |

## Oracle Database

Set in `.env`:

```
DB_ENGINE=oracle
ORACLE_NAME=ORCL
ORACLE_USER=MUUSE_TAYO_ADMIN
ORACLE_PASSWORD=your_password
ORACLE_HOST=your-host
ORACLE_PORT=1521
```

## Project Structure

- `dashboard/` — Main KPI dashboard
- `jobs/` — Job requisition management
- `applicants/` — Candidate applications
- `selection/` — Selected/hired onboarding
- `interviews/` — Interview scheduling
- `messages/` — Internal messaging
- `users/` — User administration
- `verifications/` — Pending approval gateway
- `reports/` — Analytics dashboard
- `backups/` — Excel/PDF exports
