import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

FILE_NAME = "tasks.txt"
tasks = []
selected_task_index = None
dark_mode = False


# ---------- LIGHT THEME ----------
LIGHT = {
    "PRIMARY": "#5D4E4E",
    "SECONDARY": "#FFC8DD",
    "ACCENT": "#FFD6A5",
    "SUCCESS": "#BDE0C8",
    "BACKGROUND": "#FFF8F0",
    "TEXT": "#3A3A3A",
    "CARD": "#FFFFFF",
    "SELECT": "#E7D8F5"
}


# ---------- DARK THEME ----------
DARK = {
    "PRIMARY": "#8C8282",
    "SECONDARY": "#F4A7B9",
    "ACCENT": "#FFD6A5",
    "SUCCESS": "#C4F1E1",
    "BACKGROUND": "#1E293B",
    "TEXT": "#3B3B3D",
    "CARD": "#4882A4",
    "SELECT": "#F5F5F5"   # changed to off-white
}

theme = LIGHT


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


# ---------- REFRESH TASK LIST ----------
def refresh_tasks():

    for widget in task_container.winfo_children():
        widget.destroy()

    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x["due"], "%d-%m-%Y"))

    for index, task in enumerate(sorted_tasks):

        color = theme["CARD"]

        if task["priority"] == "High":
            color = theme["SECONDARY"]
        elif task["priority"] == "Medium":
            color = theme["ACCENT"]
        elif task["priority"] == "Low":
            color = theme["SUCCESS"]

        if index == selected_task_index:
            color = theme["SELECT"]

        card = tk.Frame(task_container, bg=color, padx=20, pady=15)
        card.pack(fill="x", pady=6)

        text = f"{task['task']} | Due: {task['due']} | Priority: {task['priority']} | {task['status']}"

        label = tk.Label(
            card,
            text=text,
            bg=color,
            fg=theme["TEXT"],
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


# ---------- APPLY THEME ----------
def apply_theme():

    root.configure(bg=theme["BACKGROUND"])
    header.config(bg=theme["BACKGROUND"], fg=theme["PRIMARY"])
    input_frame.config(bg=theme["BACKGROUND"])
    button_frame.config(bg=theme["BACKGROUND"])
    task_area.config(bg=theme["BACKGROUND"])
    canvas.config(bg=theme["BACKGROUND"])
    task_container.config(bg=theme["BACKGROUND"])

    add_btn.config(bg=theme["PRIMARY"], fg="white")
    complete_btn.config(bg=theme["SUCCESS"], fg="#1A1A1A")
    delete_btn.config(bg=theme["SECONDARY"], fg="#1A1A1A")
    suggest_btn.config(bg=theme["PRIMARY"], fg="white")


# ---------- TOGGLE THEME ----------
def toggle_theme():

    global dark_mode, theme

    dark_mode = not dark_mode

    if dark_mode:
        theme = DARK
        toggle_btn.config(text="☀ Light Mode")
    else:
        theme = LIGHT
        toggle_btn.config(text="🌙 Dark Mode")

    apply_theme()
    refresh_tasks()

def suggest_schedule():

    if not tasks:
        messagebox.showinfo("Info", "No tasks available")
        return

    priority_order = {"High": 1, "Medium": 2, "Low": 3}

    sorted_tasks = sorted(
        tasks,
        key=lambda x: (
            priority_order[x["priority"]],
            datetime.strptime(x["due"], "%d-%m-%Y")
        )
    )

    result = "✨ Suggested Plan for Your Day:\n\n"

    for i, task in enumerate(sorted_tasks, 1):
        result += f"{i}. {task['task']} ({task['priority']} - {task['due']})\n"

    messagebox.showinfo("AI Task Assistant", result)


# ---------- WINDOW ----------
root = tk.Tk()
root.title("Advanced To-Do App")
root.geometry("1000x700")
root.configure(bg=theme["BACKGROUND"])


# ---------- HEADER ----------
header = tk.Label(
    root,
    text="🌸 My Productivity Planner",
    font=("Poppins SemiBold", 32),
    bg=theme["BACKGROUND"],
    fg="#6A4C93"
)

header.pack(pady=30)


# ---------- DARK MODE BUTTON ----------
toggle_btn = tk.Button(
    root,
    text="🌙 Dark Mode",
    command=toggle_theme,
    font=("Segoe UI", 10)
)

toggle_btn.pack()


# ---------- INPUT AREA ----------
input_frame = tk.Frame(root, bg=theme["BACKGROUND"])
input_frame.pack(pady=10)


tk.Label(input_frame, text="Task", bg=theme["BACKGROUND"], fg=theme["TEXT"]).grid(row=0, column=0, padx=10)

task_entry = tk.Entry(input_frame, width=35)
task_entry.grid(row=0, column=1)


tk.Label(input_frame, text="Due Date (DD-MM-YYYY)", bg=theme["BACKGROUND"], fg=theme["TEXT"]).grid(row=1, column=0)

due_entry = tk.Entry(input_frame, width=35)
due_entry.grid(row=1, column=1)


priority_var = tk.StringVar()
priority_var.set("Medium")

priority_menu = tk.OptionMenu(input_frame, priority_var, "High", "Medium", "Low")
priority_menu.grid(row=2, column=1)


# ---------- BUTTONS ----------
button_frame = tk.Frame(root, bg=theme["BACKGROUND"])
button_frame.pack(pady=20)


add_btn = tk.Button(button_frame, text="Add Task", command=add_task, width=15)
complete_btn = tk.Button(button_frame, text="Mark Completed", command=mark_completed, width=15)
delete_btn = tk.Button(button_frame, text="Delete Task", command=delete_task, width=15)

add_btn.grid(row=0, column=0, padx=10)
complete_btn.grid(row=0, column=1, padx=10)
delete_btn.grid(row=0, column=2, padx=10)

suggest_btn = tk.Button(
    root,
    text="✨ Suggest My Day",
    command=suggest_schedule,
    font=("Segoe UI", 11),
    padx=10,
    pady=5
)

suggest_btn.pack(pady=10)

# ---------- TASK AREA ----------
task_area = tk.Frame(root, bg=theme["BACKGROUND"])
task_area.pack(fill="both", expand=True, padx=100, pady=20)


canvas = tk.Canvas(task_area, bg=theme["BACKGROUND"], highlightthickness=0)
scrollbar = tk.Scrollbar(task_area, orient="vertical", command=canvas.yview)

task_container = tk.Frame(canvas, bg=theme["BACKGROUND"])

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
apply_theme()
refresh_tasks()

root.mainloop()