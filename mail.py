import json
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(title, due_date, priority):
    tasks = load_tasks()
    new_task = {
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully!")

def list_tasks(show_completed=False):
    tasks = load_tasks()
    for i, task in enumerate(tasks, 1):
        if not show_completed and task["completed"]:
            continue
        print(f"{i}. {task['title']} - Due: {task['due_date']} - Priority: {task['priority']} - Completed: {task['completed']}")

def complete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        save_tasks(tasks)
        print("Task marked as completed!")
    else:
        print("Invalid task number.")

def delete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks.pop(task_number - 1)
        save_tasks(tasks)
        print("Task deleted successfully!")
    else:
        print("Invalid task number.")

def main():
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task Title: ")
            due_date = input("Due Date (YYYY-MM-DD): ")
            priority = input("Priority (Low/Medium/High): ")
            add_task(title, due_date, priority)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_number = int(input("Enter task number to complete: "))
            complete_task(task_number)
        elif choice == "4":
            task_number = int(input("Enter task number to delete: "))
            delete_task(task_number)
        elif choice == "5":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
