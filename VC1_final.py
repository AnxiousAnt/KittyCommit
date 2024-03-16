import os
import time
import tkinter as tk
from tkinter import messagebox
import pyautogui
import pyperclip


def focus():
    time.sleep(2)
    res = pyautogui.locateCenterOnScreen("focus_grid.png", confidence=0.8)
    pyautogui.moveTo(res)
    pyautogui.click()


def commit(version_number, folder):
    commit_msg = pyautogui.prompt(text='', title='Enter the commit message')
    focus()
    pyautogui.hotkey("ctrl", "shift", "s")
    time.sleep(1)
    pyautogui.write(f'purr_{version_number}')
    pyautogui.hotkey("enter")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "shift", "s")
    time.sleep(1)
    pyautogui.write(f'v{version_number}.txt')
    pyautogui.hotkey("enter")

    # commit message file
    filename = os.path.join(folder, f"commit_msg{version_number}.txt")
    with open(filename, "w") as file:
        file.write(commit_msg)


def create_version():
    folder = folder_entry.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path")
        return

    files = os.listdir(folder)
    if not files:
        version_number = 0
    else:
        versions = [int(f[1:-4]) for f in files if f.startswith("v") and f.endswith(".txt")]
        version_number = max(versions) + 1 if versions else 0

    commit(version_number, folder)
    output_text.insert(tk.END, f"New version created: v{version_number}\n\nCommit successful!\n\n")


def copy_file_to_clipboard_and_paste(folder, file_path, version_number):
    with open(file_path, "r") as f:
        file_content = f.read()
        output_text.insert(tk.END, f"Version {version_number} source code:\n{file_content}\n")

    filename = os.path.join(folder, f"commit_msg{version_number}.txt")
    with open(filename, "r") as file:
        content = file.read()
        output_text.insert(tk.END, f"Commit Message for version {version_number}:\n{content}\n\n")

    pyperclip.copy(file_content)
    time.sleep(2)
    res = pyautogui.locateCenterOnScreen("focus_grid.png", confidence=0.8)
    pyautogui.moveTo(res)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("del")
    time.sleep(1)
    pyautogui.hotkey("alt", "ctrl", "v")
    pyautogui.moveTo(res)
    pyautogui.click()


def display_version():
    folder = folder_entry.get()
    version_number = version_entry.get()
    filename = os.path.join(folder, f"v{version_number}.txt")
    if os.path.exists(filename):
        copy_file_to_clipboard_and_paste(folder, filename, version_number)
    else:
        output_text.insert(tk.END, f"Version {version_number} does not exist.\n")


def exit_program():
    root.destroy()


root = tk.Tk()
root.title("KittyCommit - Version Control for Purr-Data")

# Title Label
title_label = tk.Label(root, text="KittyCommit - Version Control for Purr-Data", font=("Arial", 14, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Folder Entry
folder_label = tk.Label(root, text="Enter folder path for purr-data files:")
folder_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=1, column=1, padx=10, pady=10)

# Create Version Frame
create_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
create_frame.grid(row=2, column=0, padx=10, pady=10)

create_button = tk.Button(create_frame, text="Create New Version", command=create_version)
create_button.pack(padx=10, pady=5)

# Version Entry
version_label = tk.Label(root, text="Enter version number to display:")
version_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
version_entry = tk.Entry(root, width=20)
version_entry.grid(row=3, column=1, padx=10, pady=10)

# Display Version Frame
display_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
display_frame.grid(row=4, column=0, padx=10, pady=10)

display_label = tk.Label(display_frame, text="Display commits")
display_label.pack(padx=10, pady=5)

display_button = tk.Button(display_frame, text="Display Version", command=display_version)
display_button.pack(padx=10, pady=5)

# Output Console Label
output_label = tk.Label(root, text="Output Console", font=("Arial", 12, "bold"))
output_label.grid(row=5, column=0, pady=10)

# Output Text
output_text = tk.Text(root, width=60, height=20, bd=2, relief=tk.GROOVE)
output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.grid(row=7, column=1, pady=10)

root.mainloop()
