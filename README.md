# Olympiad Training Sets Database

Math Olympiad trainers often train multiple different teams over a single training cycle. To ensure that problems are not repeated over different training sets for the same trainees, we built a simple database system to check for when each problem is used in previous training sessions.

The database uses three tables to keep track of the many-to-many relationship between problems and sessions:

```sql
-- Table of all unique math problems
CREATE TABLE IF NOT EXISTS problems (
    problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT,
    contest TEXT,
    year INTEGER,
    problem_number TEXT,
    difficulty INTEGER
);

-- Table of all training sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    demographic TEXT,
    training_type TEXT,
    session_date TEXT
);

-- Junction table of all instances of a problem being featured in a session
CREATE TABLE IF NOT EXISTS problem_session (
    problem_id INTEGER,
    session_id INTEGER,
    PRIMARY KEY (problem_id, session_id),
    FOREIGN KEY (problem_id) REFERENCES problems (problem_id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
);
```

       ┌────────────────────┐                 ┌───────────────────┐
       │     problems       │                 │     sessions      │
       ├────────────────────┤                 ├───────────────────┤
       │ PK │ problem_id    │                 │ PK │ session_id   │
       │    │ country_code  │                 │    │ demographic  │
       │    │ contest       │                 │    │ training_type│
       │    │ year          │                 │    │ session_date │
       │    │ problem_number│                 └───────────────────┘
       │    │ difficulty    │                           │
       └────────────────────┘                           │
                 │                                      │
                 │ (1)                                  │ (1)
                 │                                      │
                 └───┐                             ┌────┘
                     │                             │
                     ▼ (M)                         ▼ (M)
               ┌─────────────────────────────────────────┐
               │             problem_session             │
               ├─────────────────────────────────────────┤
               │ PK, FK1 │  problem_id                   │
               │ PK, FK2 │  session_id                   │
               └─────────────────────────────────────────┘

## Usage

The `initialise.py` file initialises the database.

The `update.py` file logs a new training set. To log the new training set, we input the problems' details into the `logs/problems.csv` file, and the session details into the `logs/session.csv` file.

In `database_utils.py`, the functions `log_training_session`, `get_problems`, `get_sessions` are defined. The first is used by `update.py` to log a new training set. The `get_problems` function is used to query for all problems in a certain training session. The `get_sessions` function is used to query for all sessions in which a problem has appeared in.