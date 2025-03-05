from datetime import datetime
from enum import Enum
from the_procrastination_terminator.categories import TaskCategory

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task:
    def __init__(self, user_id, title, description, deadline, priority, category: TaskCategory):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        self.priority = Priority(priority)
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d %H:%M"),
            "priority": self.priority.value,
            "category": self.category.get_display_name(),
            "completed": self.completed
        }

class TaskManager:
    def __init__(self, db_adapter):
        self.db_adapter = db_adapter
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.db_adapter.save_task(task)

    def remove_task(self, task):
        self.tasks.remove(task)
        # TODO: Реализовать удаление задачи из базы данных

    def get_stats(self):
        completed_tasks = [task for task in self.tasks if task.completed]
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return "Нет задач"
        completion_rate = len(completed_tasks) / total_tasks * 100
        return f"Выполнено: {len(completed_tasks)}/{total_tasks} ({completion_rate:.2f}%)"
