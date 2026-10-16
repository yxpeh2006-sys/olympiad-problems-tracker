from sqlalchemy import create_engine, text

connection_url = "sqlite:///olympiad.db"
engine = create_engine(connection_url)

with engine.connect() as conn:
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS problems (
            problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code TEXT,
            contest TEXT,
            year INTEGER,
            problem_number TEXT,
            difficulty INTEGER,
            genre TEXT
        );
        """
    ))

    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            demographic TEXT,
            training_type TEXT,
            session_date TEXT
        )
        """
    ))

    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS problem_session (
            problem_id INTEGER,
            session_id INTEGER,
            PRIMARY KEY (problem_id, session_id)
            FOREIGN KEY (problem_id) REFERENCES problems (problem_id) ON DELETE CASCADE,
            FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
        )
        """
    ))
