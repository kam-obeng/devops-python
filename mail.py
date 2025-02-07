import json
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from tkcalendar import Calendar
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        # Load tasks on start
        self.tasks = self.load_tasks()
        
        # UI Setup
        self.setup_ui()

    def load_tasks(self):
        """Loads tasks from a JSON file."""
        try:
            with open(TASKS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        """Saves tasks to a JSON file."""
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        """Opens a dialog to add a new task using a calendar for date selection."""
        add_window = Toplevel(self.root)
        add_window.title("Add Task")
        add_window.geometry("300x320")

        tk.Label(add_window, text="Task Title:").pack(pady=5)
        title_entry = tk.Entry(add_window)
        title_entry.pack(pady=5)

        tk.Label(add_window, text="Due Date:").pack(pady=5)
        cal = Calendar(add_window, date_pattern="dd-mm-yyyy")  # Calendar widget
        cal.pack(pady=5)

        tk.Label(add_window, text="Priority:").pack(pady=5)
        priority_var = tk.StringVar(value="Medium")
        
        priority_frame = tk.Frame(add_window)
        tk.Radiobutton(priority_frame, text="Low", variable=priority_var, value="Low").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value="Medium").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(priority_frame, text="High", variable=priority_var, value="High").pack(side=tk.LEFT, padx=5)
        priority_frame.pack(pady=5)

        def save_task():
            title = title_entry.get()
            due_date = cal.get_date()  # Get selected date from calendar
            priority = priority_var.get()

            if not title:
                messagebox.showwarning("Input Error", "Task title cannot be empty!")
                return

            formatted_date = datetime.strptime(due_date, "%d-%m-%Y").strftime("%Y-%m-%d")  # Convert for sorting

            new_task = {
                "title": title,
                "due_date": formatted_date,  # Stored in YYYY-MM-DD format for sorting
                "priority": priority,
                "completed": False
            }
            self.tasks.append(new_task)
            self.tasks.sort(key=lambda x: (x["completed"], x["due_date"], x["priority"]))
            self.save_tasks()
            self.update_task_list()
            add_window.destroy()

        tk.Button(add_window, text="Save Task", command=save_task).pack(pady=10)

    def list_tasks(self):
        """Displays tasks in the listbox with European date format (DD-MM-YYYY)."""
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks, 1):
            status = "✔" if task["completed"] else "✘"
            display_date = datetime.strptime(task["due_date"], "%Y-%m-%d").strftime("%d-%m-%Y")
            display_text = f"{i}. {task['title']} - Due: {display_date} - Priority: {task['priority']} - {status}"
            self.task_listbox.insert(tk.END, display_text)
            
            # Colour coding based on priority
            if task["priority"] == "High":
                self.task_listbox.itemconfig(tk.END, {'fg': 'red'})
            elif task["priority"] == "Medium":
                self.task_listbox.itemconfig(tk.END, {'fg': 'orange'})
            else:
                self.task_listbox.itemconfig(tk.END, {'fg': 'green'})

    def complete_task(self):
        """Marks a selected task as completed."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.save_tasks()
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to complete!")

    def delete_task(self):
        """Deletes a selected task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.save_tasks()
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")

    def update_task_list(self):
        """Updates the task list UI."""
        self.list_tasks()

    def setup_ui(self):
        """Sets up the GUI layout."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(frame, width=60, height=10, yscrollcommand=scrollbar.set)
        self.task_listbox.pack()
        scrollbar.config(command=self.task_listbox.yview)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Complete Task", command=self.complete_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=0, column=3, padx=5)

        self.update_task_list()

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()