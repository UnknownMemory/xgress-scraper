from pathlib import Path
import sqlite3

ROOT_DIR: Path = Path(__file__).parent.parent.absolute()


class Database:

    def __init__(self) -> None:
        self.con: sqlite3.Connection = sqlite3.connect(f'{ROOT_DIR}/xgress.db', isolation_level=None)
        self.cursor = self.con.cursor()
        self._init_db()

    def _init_db(self) -> None:
        print("Database Initialization...\n")

        # optimization
        self.cursor.execute('PRAGMA journal_mode = OFF;')
        self.cursor.execute('PRAGMA synchronous = 0;')
        self.cursor.execute('PRAGMA cache_size = 1000000;')
        self.cursor.execute('PRAGMA locking_mode = EXCLUSIVE;')
        self.cursor.execute('PRAGMA temp_store = MEMORY;')

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

    def begin_transaction(self, batch: list[tuple]) -> str:
        self.cursor.execute('BEGIN')
        self.cursor.executemany(
            'INSERT INTO location (name, pguid, short, img, address, description, lon, lat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            batch)

        return "Transaction added"

    def end_transaction(self) -> str:
        try:
            self.con.commit()
        except sqlite3.OperationalError:
            self.con.rollback()
            return 'Failed to commit transactions\n'

        return "Data successfully saved to the database\n"
