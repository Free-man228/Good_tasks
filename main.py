import json
import os


def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def add_task(tasks):
    title = input("Введите название задачи: ")
    task = {"id": len(tasks) + 1, "title": title, "completed": False}
    tasks.append(task)
    print(f"Задача '{title}' добавлена!")


def view_tasks(tasks):
    if not tasks:
        print("Список задач пуст!")
        return
    for task in tasks:
        status = "Выполнено" if task["completed"] else "Не выполнено"
        print(f"{task['id']}. {task['title']} - {status}")


def complete_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("Введите номер задачи для отметки как выполненной: "))
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                print(f"Задача '{task['title']}' отмечена как выполненная!")
                return
        print("Задача с таким номером не найдена!")
    except ValueError:
        print("Пожалуйста, введите число!")


def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_id = int(input("Введите номер задачи для удаления: "))
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(i)
                print(f"Задача '{task['title']}' удалена!")
                return
        print("Задача с таким номером не найдена!")
    except ValueError:
        print("Пожалуйста, введите число!")


def main():
    tasks = load_tasks()
    while True:
        print("\n1. Добавить задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Удалить задачу")
        print("5. Выйти")
        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Программа завершена!")
            break
        else:
            print("Неверный выбор, попробуйте снова!")
        save_tasks(tasks)


if __name__ == "__main__":
    main()