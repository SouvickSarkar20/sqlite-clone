# 🗄️ SQLite Clone — A Hand-Built Database Engine

A simple database engine built from scratch in Python, for learning purposes.  
Type SQL in your browser. Data gets stored in a binary file on disk.  
No ORMs. No external database libraries. Just code.

---

## What This Is

This project implements the core ideas behind how SQLite works internally:

- **A Pager** — manages reading and writing 4KB pages to/from a `.db` binary file
- **A Serializer** — converts Python dicts (rows) into bytes and back
- **A B-Tree** — indexes rows so lookups are fast (O log n, not O n)
- **A SQL Parser** — reads SQL strings and turns them into structured commands
- **A Query Executor** — connects the parser output to the right B-Tree operation
- **A Flask Web UI** — so you can type SQL in a browser and see results

---

## Supported SQL

```sql
CREATE TABLE users (id, name, age)

INSERT INTO users VALUES (1, 'alice', 25)

SELECT * FROM users

SELECT * FROM users WHERE id = 1

DELETE FROM users WHERE id = 1
```

---

## Project Structure

```
sqlite-clone/
│
├── core/
│   ├── pager.py        # Reads/writes pages from the .db file
│   ├── serializer.py   # Converts rows ↔ bytes
│   ├── btree.py        # B-Tree: insert, search, traverse
│   └── executor.py     # Runs queries against the right table
│
├── sql/
│   └── parser.py       # Turns SQL string → Python dict
│
├── web/
│   ├── app.py          # Flask server + API endpoint
│   ├── templates/
│   │   └── index.html  # The browser UI
│   └── static/
│       └── style.css   # Styling
│
├── data/
│   └── mydb.db         # The actual binary database file (created on first run)
│
├── tests/              # pytest test suite, one file per module
├── requirements.txt
└── README.md
```

---

## How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/sqlite-clone.git
cd sqlite-clone
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the server**
```bash
python web/app.py
```

**5. Open your browser**
```
http://localhost:5000
```

---

## How to Run Tests

```bash
pytest tests/
```

---

## How It Works — The Flow

```
You type SQL in the browser
        ↓
Flask receives the string  (web/app.py)
        ↓
Parser reads it            (sql/parser.py)   → { type: INSERT, table: users, ... }
        ↓
Executor decides what to do (core/executor.py)
        ↓
B-Tree finds/stores the row (core/btree.py)
        ↓
Serializer converts it      (core/serializer.py) → bytes
        ↓
Pager writes to disk        (core/pager.py)
        ↓
data/mydb.db  ← your data lives here
```

---

## Build Phases

| Phase | What was built | Status |
|-------|---------------|--------|
| 0 | Project skeleton, folder structure, Flask hello world | ✅ Done |
| 1 | Pager — file I/O and page caching | 🔧 In progress |
| 2 | Serializer — row ↔ bytes conversion | ⏳ Upcoming |
| 3 | B-Tree — insert, search, traversal | ⏳ Upcoming |
| 4 | SQL Parser — string → structured command | ⏳ Upcoming |
| 5 | Executor — query engine connecting all layers | ⏳ Upcoming |
| 6 | Web UI — results table, error handling | ⏳ Upcoming |
| 7 | Deploy to Render | ⏳ Upcoming |

---

## Why I Built This

To understand how databases actually work under the hood — not just how to use them.  
Most developers use databases every day without knowing what happens when you call `INSERT`.  
This project is my answer to that question.

---

## Tech Stack

- **Python 3.11+**
- **Flask** — web server
- **struct** — binary serialization
- **pytest** — testing
- No database libraries used anywhere.