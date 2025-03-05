import yaml
import logging
from dotenv import load_dotenv
from the_procrastination_terminator.bot import Bot

# Загрузка конфигурации
load_dotenv()
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Запуск бота
if __name__ == "__main__":
    bot_instance = Bot(config)
    bot_instance.start()
