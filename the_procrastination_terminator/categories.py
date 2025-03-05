from abc import ABC, abstractmethod

class TaskCategory(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_display_name(self):
        pass

class WorkCategory(TaskCategory):
    def __init__(self):
        super().__init__("Работа")
    def get_display_name(self):
        return self.name

class StudyCategory(TaskCategory):
    def __init__(self):
        super().__init__("Учёба")
    def get_display_name(self):
        return self.name

class PersonalCategory(TaskCategory):
    def __init__(self):
        super().__init__("Личное")
    def get_display_name(self):
        return self.name
