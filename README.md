# Sky Engineering Portal

A web application built for Sky's Engineering Department to replace their internal Excel spreadsheet. The idea is simple — instead of a shared spreadsheet that anyone can accidentally break, this gives engineers a proper portal to look up teams, understand dependencies, schedule meetings, and message each other directly.

Built with Django and SQLite as part of a university group project.

---

## What it does

- **Teams** — browse all engineering teams, see who's in them, what they do, and how they depend on each other
- **Departments & Organisation** — view the org structure and how teams relate
- **Messages** — send internal messages between users, with inbox, sent, drafts and reply support
- **Schedule** — book meetings with date, time, platform and attendees, with weekly and monthly calendar views
- **Reports** — generate summaries of teams and departments
- **Django Admin** — full admin panel for managing everything behind the scenes

---

## Tech stack

- Python 3.12
- Django 6.0.4
- SQLite
- Bootstrap 5.3
- Bootstrap Icons

---

## Getting it running

**1. Clone the repo**
```bash
git clone https://github.com/serge-yetimian/skyengineering.git
cd skyengineering
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Create an admin account**
```bash
python manage.py createsuperuser
```

**6. Start the server**
```bash
python manage.py runserver
```

Then open http://127.0.0.1:8000 in your browser.

---

## Project structure

```
skyengineering-main/
├── messaging/        # Student 3 — internal messaging system
├── schedule/         # Student 4 — meeting scheduler
├── skyengineering/   # Django project settings and URLs
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## The team

This was built as a group project for 5COSC021W Software Development Group Project at the University of Westminster. Each team member was responsible for a different part of the application.

| Student | Feature |
|---------|---------|
| Student 1 | Teams |
| Student 2 | Organisation & Departments |
| Student 3 | Messaging |
| Student 4 | Schedule |
| Student 5 | Reports |
| Student 6 | Data Visualisation |

---

## Notes

- This is a development build — not intended for production use
- The admin panel is available at `/admin/`
- Default login page is at `/accounts/login/`
