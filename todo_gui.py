import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

FILE_NAME = "tasks.txt"
tasks = []
selected_task_index = None


# ---------- PASTEL THEME ----------
PRIMARY = "#CDB4DB"       # lavender
SECONDARY = "#FFC8DD"     # blush pink
ACCENT = "#FFD6A5"        # peach
SUCCESS = "#BDE0C8"       # mint
BACKGROUND = "#FFF8F0"    # cream

TEXT = "#3A3A3A"
CARD = "#FFFFFF"
SELECT = "#E7D8F5"


# ---------- LOAD TASKS ----------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                task, status, due, priority = line.strip().split("|")
                tasks.append({
                    "task": task,
                    "status": status,
                    "due": due,
                    "priority": priority
                })


# ---------- SAVE TASKS ----------
def save_tasks():
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(
                f"{task['task']}|{task['status']}|{task['due']}|{task['priority']}\n"
            )


# ---------- SELECT TASK ----------
def select_task(index):
    global selected_task_index
    selected_task_index = index
    refresh_tasks()


# ---------- REFRESH TASKS ----------
def refresh_tasks():

    for widget in task_container.winfo_children():
        widget.destroy()

    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["due"], "%d-%m-%Y"))

    for index, task in enumerate(sorted_tasks):

        color = CARD

        if task["priority"] == "High":
            color = SECONDARY
        elif task["priority"] == "Medium":
            color = ACCENT
        elif task["priority"] == "Low":
            color = SUCCESS

        if index == selected_task_index:
            color = SELECT

        card = tk.Frame(
            task_container,
            bg=color,
            padx=20,
            pady=15
        )

        card.pack(fill="x", pady=6)

        text = f"{task['task']}    |    Due: {task['due']}    |    Priority: {task['priority']}    |    {task['status']}"

        label = tk.Label(
            card,
            text=text,
            bg=color,
            fg=TEXT,
            font=("Segoe UI", 11),
            anchor="w"
        )

        label.pack(fill="x")

        card.bind("<Button-1>", lambda e, i=index: select_task(i))
        label.bind("<Button-1>", lambda e, i=index: select_task(i))


# ---------- ADD TASK ----------
def add_task():

    task_name = task_entry.get()
    due_date = due_entry.get()
    priority = priority_var.get()

    if task_name == "" or due_date == "":
        messagebox.showerror("Error", "Task and date required")
        return

    try:
        datetime.strptime(due_date, "%d-%m-%Y")
    except:
        messagebox.showerror("Error", "Date must be DD-MM-YYYY")
        return

    tasks.append({
        "task": task_name,
        "status": "Pending",
        "due": due_date,
        "priority": priority
    })

    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)


# ---------- MARK COMPLETE ----------
def mark_completed():

    global selected_task_index

    if selected_task_index is None:
        messagebox.showwarning("Warning", "Select a task")
        return

    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["due"], "%d-%m-%Y"))

    selected = sorted_tasks[selected_task_index]

    for task in tasks:
        if task == selected:
            task["status"] = "Completed"

    save_tasks()

    selected_task_index = None
    refresh_tasks()


# ---------- DELETE TASK ----------
def delete_task():

    global selected_task_index

    if selected_task_index is None:
        messagebox.showwarning("Warning", "Select a task")
        return

    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["due"], "%d-%m-%Y"))

    selected = sorted_tasks[selected_task_index]

    tasks.remove(selected)

    save_tasks()

    selected_task_index = None
    refresh_tasks()


# ---------- WINDOW ----------
root = tk.Tk()
root.title("Advanced To-Do App")
root.geometry("1000x700")
root.configure(bg=BACKGROUND)


# ---------- HEADER ----------
header = tk.Label(
    root,
    text="🌸 My Productivity Planner",
    font=("Segoe UI", 26, "bold"),
    bg=BACKGROUND,
    fg="#6A4C93"
)

header.pack(pady=30)


# ---------- INPUT AREA ----------
input_frame = tk.Frame(root, bg=BACKGROUND)
input_frame.pack(pady=10)


tk.Label(input_frame, text="Task", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 12)).grid(row=0, column=0, padx=10)

task_entry = tk.Entry(input_frame, width=35, font=("Segoe UI", 11))
task_entry.grid(row=0, column=1, padx=10)


tk.Label(input_frame, text="Due Date (DD-MM-YYYY)", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 12)).grid(row=1, column=0, pady=10)

due_entry = tk.Entry(input_frame, width=35, font=("Segoe UI", 11))
due_entry.grid(row=1, column=1)


tk.Label(input_frame, text="Priority", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 12)).grid(row=2, column=0)

priority_var = tk.StringVar()
priority_var.set("Medium")

priority_menu = tk.OptionMenu(input_frame, priority_var, "High", "Medium", "Low")
priority_menu.config(width=32)
priority_menu.grid(row=2, column=1)


# ---------- BUTTONS ----------
button_frame = tk.Frame(root, bg=BACKGROUND)
button_frame.pack(pady=20)


tk.Button(
    button_frame,
    text="Add Task",
    bg=PRIMARY,
    fg="white",
    width=15,
    font=("Segoe UI", 11),
    command=add_task
).grid(row=0, column=0, padx=10)


tk.Button(
    button_frame,
    text="Mark Completed",
    bg=SUCCESS,
    fg=TEXT,
    width=15,
    font=("Segoe UI", 11),
    command=mark_completed
).grid(row=0, column=1, padx=10)


tk.Button(
    button_frame,
    text="Delete Task",
    bg=SECONDARY,
    fg=TEXT,
    width=15,
    font=("Segoe UI", 11),
    command=delete_task
).grid(row=0, column=2, padx=10)


# ---------- TASK AREA ----------
task_area = tk.Frame(root, bg=BACKGROUND)
task_area.pack(fill="both", expand=True, padx=100, pady=20)


canvas = tk.Canvas(task_area, bg=BACKGROUND, highlightthickness=0)
scrollbar = tk.Scrollbar(task_area, orient="vertical", command=canvas.yview)

task_container = tk.Frame(canvas, bg=BACKGROUND)

task_container.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=task_container, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# ---------- START ----------
load_tasks()
refresh_tasks()

root.mainloop()