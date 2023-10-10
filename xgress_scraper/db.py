from pathlib import Path
import sqlite3

ROOT_DIR: Path = Path(__file__).parent.parent.absolute()


class Database:

    def __init__(self) -> None:
        self.con: sqlite3.Connection = sqlite3.connect(f'{ROOT_DIR}/xgress.db')
        self.cursor = self.con.cursor()
        self._init_db()

    def _init_db(self) -> None:
        print("Database Initialization...\n")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pguid TEXT NOT NULL UNIQUE,
            short TEXT NOT NULL,
            img TEXT NOT NULL,
            address TEXT NOT NULL,
            description TEXT,
            lon REAL NOT NULL,
            lat REAL NOT NULL,
            UNIQUE(lon, lat) ON CONFLICT IGNORE)
            ''')
        self.con.commit()
