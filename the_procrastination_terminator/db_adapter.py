from abc import ABC, abstractmethod
import sqlite3

class DatabaseAdapter(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def save_task(self, task):
        pass

    @abstractmethod
    def load_tasks(self, user_id):
        pass

class SQLiteAdapter(DatabaseAdapter):
    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                description TEXT,
                deadline TEXT,
                priority TEXT,
                category TEXT,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def save_task(self, task):
        self.cursor.execute(
            """
            INSERT INTO tasks (user_id, title, description, deadline, priority, completed)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task.user_id,
                task.title,
                task.description,
                task.deadline.strftime("%Y-%m-%d %H:%M"),
                task.priority.value,  # передаем строковое значение Enuma
                int(task.completed)
            )
        )

    def load_tasks(self, user_id):
        self.cursor.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()
