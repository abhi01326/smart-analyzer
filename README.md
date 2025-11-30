# Smart Task Analyzer  
A mini full-stack application built using **Python**, **Django**, and **HTML/JS** that intelligently scores and prioritizes tasks using a multi-factor algorithm.

This project was built as part of a technical assessment for a **Software Development Intern** position.

---

# 📌 Features

### ✔ Intelligent Task Scoring  
Each task receives a score based on:
- **Urgency** (due date proximity)
- **Importance** (1–10 user rating)
- **Effort** (lower hours = higher priority)
- **Dependencies** (tasks that block others get boosted)

### ✔ Sorting Strategy Modes  
Users can switch between:
- **Smart Balance** (all factors weighted)
- **Fastest Wins** (low effort first)
- **High Impact** (importance first)
- **Deadline Driven** (due date first)

### ✔ API Endpoints
- `POST /api/tasks/analyze/`  
  Returns sorted list of tasks with scores  
- `POST /api/tasks/suggest/`  
  Returns top 3 task suggestions

### ✔ Frontend Features
- Add individual tasks
- Paste JSON for bulk import
- Choose scoring strategy
- View sorted results with scores
- Responsive + clean UI

---

# 🚀 Getting Started

## 1. Clone the Repo
```bash
git clone <your-repository-url>
cd task-analyzer/backend


task-analyzer/
│
├── backend/
│   ├── manage.py
│   ├── task_analyzer/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── tasks/
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── scoring.py
│       ├── views.py
│       ├── urls.py
│       └── tests.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
└── README.md
