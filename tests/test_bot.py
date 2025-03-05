import unittest
from the_procrastination_terminator.tasks import Task, TaskManager
from the_procrastination_terminator.db_adapter import SQLiteAdapter

class TestBot(unittest.TestCase):
    """Набор тестов для проверки базовой логики Task и TaskManager."""

    def setUp(self):
        """
        Запускается перед каждым тестом.
        Создаём in-memory базу данных (':memory:'),
        чтобы не портить реальные файлы.
        """
        self.db_adapter = SQLiteAdapter(':memory:')
        self.task_manager = TaskManager(self.db_adapter)

    def test_add_task(self):
        """
        Проверяем, что после добавления задачи
        она действительно сохраняется в базе данных.
        """
        task = Task(
            user_id=123,
            title='Test Task',
            description='Test Description',
            deadline='2025-03-10 09:00',
            priority='high',
            category='Test Category'
        )
        self.task_manager.add_task(task)

        # Загружаем все задачи для пользователя 123
        tasks = self.db_adapter.load_tasks(123)

        # Убеждаемся, что задача действительно сохранилась
        self.assertEqual(len(tasks), 1, 'Должна быть ровно одна задача в базе')

        # Проверяем, что поля совпадают
        saved_task = tasks[0]
        self.assertEqual(saved_task[2], 'Test Task', 'Название задачи не совпадает')
        self.assertEqual(saved_task[3], 'Test Description', 'Описание задачи не совпадает')

if __name__ == '__main__':
    unittest.main()
