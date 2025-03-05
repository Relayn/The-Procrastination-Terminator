import os
import telebot
from dotenv import load_dotenv
from telebot import types
from the_procrastination_terminator.tasks import Task, TaskManager, Priority
from the_procrastination_terminator.db_adapter import SQLiteAdapter
from the_procrastination_terminator.categories import WorkCategory, StudyCategory, PersonalCategory

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Используем один экземпляр TeleBot
bot = telebot.TeleBot(TOKEN)

# Инициализируем базу данных и менеджер задач
db_adapter = SQLiteAdapter()
task_manager = TaskManager(db_adapter)

# Словарь для хранения временных данных пользователя
user_temp_data = {}


class Bot:
    def __init__(self, config):
        self.config = config
        # Используем уже созданный глобальный экземпляр bot
        self.bot = bot

    def start(self):
        print("🤖 Бот запущен!")
        self.bot.polling(none_stop=True)


# ---------------------
# Обработчики команд:

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я The Procrastination Terminator! 💪\n"
        "Вот мои команды:\n"
        "/add - Добавить задачу\n"
        "/list - Показать задачи с быстрым управлением"
    )


@bot.message_handler(commands=['add'])
def add_task(message):
    bot.reply_to(
        message,
        "Введите задачу в формате:\n"
        "Название | Описание | Дата (YYYY-MM-DD HH:MM) | Приоритет (high/medium/low) | Категория (work/study/personal)"
    )
    user_temp_data[message.chat.id] = "waiting_for_task"


@bot.message_handler(func=lambda message: user_temp_data.get(message.chat.id) == "waiting_for_task")
def process_task_input(message):
    try:
        title, description, deadline, priority, category_str = map(str.strip, message.text.split("|"))
        category = {
            "work": WorkCategory(),
            "study": StudyCategory(),
            "personal": PersonalCategory()
        }.get(category_str.lower(), None)

        if not category:
            bot.reply_to(message, "Ошибка: Категория должна быть work, study или personal.")
            return

        # Создаем объект задачи. Предполагается, что Task сам преобразует deadline в datetime.
        task = Task(message.chat.id, title, description, deadline, priority, category)

        # Сохраняем задачу в БД
        task_manager.add_task(task)
        bot.reply_to(message, f"✅ Задача '{title}' добавлена!")
    except Exception as e:
        bot.reply_to(message, f"⚠ Ошибка при добавлении задачи: {e}")
    finally:
        user_temp_data.pop(message.chat.id, None)


@bot.message_handler(commands=['list'])
def list_tasks(message):
    tasks = task_manager.db_adapter.load_tasks(message.chat.id)
    if not tasks:
        bot.reply_to(message, "📭 У вас нет активных задач.")
        return

    for task in tasks:
        # task: (id, user_id, title, description, deadline, priority, category, completed)
        markup = types.InlineKeyboardMarkup()
        # Если задача не завершена, добавляем кнопку для завершения
        if not task[7]:
            complete_button = types.InlineKeyboardButton(
                text="Завершить", callback_data=f"complete_{task[0]}"
            )
            markup.add(complete_button)
        # Добавляем кнопку для удаления задачи
        delete_button = types.InlineKeyboardButton(
            text="Удалить", callback_data=f"delete_{task[0]}"
        )
        markup.add(delete_button)
        status = "✅" if task[7] else "⏳"
        text = f"{task[2]} | {task[4]} | {status}"
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("complete_") or call.data.startswith("delete_"))
def callback_inline(call):
    if call.data.startswith("complete_"):
        try:
            task_id = int(call.data.split("_")[1])
            task_manager.db_adapter.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
            task_manager.db_adapter.conn.commit()
            bot.answer_callback_query(call.id, "Задача завершена!")
            # Обновляем сообщение: убираем inline-клавиатуру
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.send_message(call.message.chat.id, "✅ Задача отмечена как завершённая!")
        except Exception as e:
            bot.answer_callback_query(call.id, f"Ошибка: {e}")
    elif call.data.startswith("delete_"):
        try:
            task_id = int(call.data.split("_")[1])
            task_manager.db_adapter.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            task_manager.db_adapter.conn.commit()
            bot.answer_callback_query(call.id, "Задача удалена!")
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.send_message(call.message.chat.id, "✅ Задача удалена!")
        except Exception as e:
            bot.answer_callback_query(call.id, f"Ошибка: {e}")


if __name__ == "__main__":
    bot.polling()
