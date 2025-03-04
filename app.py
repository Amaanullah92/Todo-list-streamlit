import streamlit as st
import emoji
import os

# File to store tasks
TASKS_FILE = "tasks.txt"

# Load tasks from TXT file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    
    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    tasks = []
    for line in lines:
        line = line.strip()
        if line:
            completed = line.startswith("[✔]")  
            task_text = line[4:].strip()  
            tasks.append({"task": task_text, "completed": completed})
    return tasks

# Save tasks to TXT file
def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        for task in tasks:
           status = "[\u2714]" if task["completed"] else "[ ]"
           file.write(f"{status} {task['task']}\n")

# Initialize task list
tasks = load_tasks()

# Streamlit UI
st.title(emoji.emojize(":pushpin: To-Do List with TXT Saving"))  # 📌 Dynamic Emoji

# Input for new task
new_task = st.text_input("Enter a new task:")
if st.button("Add Task"):
    if new_task.strip():
        tasks.append({"task": new_task.strip(), "completed": False})
        save_tasks(tasks)
        st.rerun()

# Display tasks
st.subheader("Your Tasks:")
for i, task in enumerate(tasks):
    col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
    
    completed = col1.checkbox(task["task"], task["completed"], key=f"task_{i}")
    if completed != task["completed"]:
        tasks[i]["completed"] = completed
        save_tasks(tasks)
        st.rerun()

    # ❌ Cross Emoji Dynamically
    if col2.button(emoji.emojize(":cross_mark:"), key=f"delete_{i}"):
        tasks.pop(i)
        save_tasks(tasks)
        st.rerun()

# Download TXT file
with open(TASKS_FILE, "rb") as file:
    st.download_button(emoji.emojize(":inbox_tray: Download Task List (TXT)"), file, file_name="tasks.txt", mime="text/plain")

# Clear all tasks
if st.button("Clear All Tasks"):
    tasks = []
    save_tasks(tasks)
    st.rerun()