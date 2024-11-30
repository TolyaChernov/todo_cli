import json
from typing import Dict, List, Optional


class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: str,
        completed: bool = False,
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed,
        }


class TaskManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(
        self, title: str, description: str, category: str, due_date: str, priority: str
    ) -> Task:
        task_id = len(self.tasks) + 1
        new_task = Task(
            task_id,
            title,
            description,
            category,
            due_date,
            priority)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def mark_task_completed(self, task_id: int):
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self.save_tasks()

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self.save_tasks()

    def search_tasks(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        result = self.tasks
        if keyword:
            result = [task for task in result if keyword.lower()
                      in task.title.lower()]

        if category:
            result = [
                task for task in result if task.category.lower() == category.lower()
            ]

        if completed is not None:
            result = [task for task in result if task.completed == completed]

        return result

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None


def main():
    manager = TaskManager("tasks.json")

    while True:
        print("\nМенеджер задач")
        print("1. Посмотреть все задачи")
        print("2. Добавить задачу")
        print("3. Пометить задачу как выполненную")
        print("4. Удалить задачу")
        print("5. Искать задачи")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            for task in manager.tasks:
                status = "✓" if task.completed else "✗"
                print(
                    f"{task.task_id}: {task.title} [{status}] | {task.category} | "
                    f"{task.due_date} | {task.priority}"
                )

        elif choice == "2":
            title = input("Название задачи: ")
            description = input("Описание задачи: ")
            category = input("Категория задачи: ")
            due_date = input("Срок выполнения (ГГГГ-ММ-ДД): ")
            priority = input("Приоритет (низкий, средний, высокий): ")
            manager.add_task(title, description, category, due_date, priority)
            print("Задача добавлена.")

        elif choice == "3":
            task_id = int(input("Введите ID задачи для завершения: "))
            manager.mark_task_completed(task_id)
            print("Задача помечена как выполненная.")

        elif choice == "4":
            task_id = int(input("Введите ID задачи для удаления: "))
            manager.delete_task(task_id)
            print("Задача удалена.")

        elif choice == "5":
            keyword = input(
                "Введите ключевое слово для поиска (или оставьте пустым): ")
            category = input(
                "Введите категорию для поиска (или оставьте пустым): ")
            completed = input("Отображать выполненные задачи? (да/нет): ")
            completed = completed.lower() == "да"
            results = manager.search_tasks(
                keyword or None, category or None, completed if completed else None
            )
            for task in results:
                status = "✓" if task.completed else "✗"
                print(
                    f"{task.task_id}: {task.title} [{status}] | {task.category} | "
                    f"{task.due_date} | {task.priority}"
                )

        elif choice == "6":
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
