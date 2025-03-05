from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class ReminderStrategy(ABC):
    @abstractmethod
    def calculate_reminder_time(self, deadline):
        pass

class OneDayReminder(ReminderStrategy):
    def calculate_reminder_time(self, deadline):
        return deadline - timedelta(days=1)

class OneHourReminder(ReminderStrategy):
    def calculate_reminder_time(self, deadline):
        return deadline - timedelta(hours=1)

class FifteenMinuteReminder(ReminderStrategy):
    def calculate_reminder_time(self, deadline):
        return deadline - timedelta(minutes=15)

class OneWeekReminder(ReminderStrategy):
    def calculate_reminder_time(self, deadline):
        return deadline - timedelta(weeks=1)
