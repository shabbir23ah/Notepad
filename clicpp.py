import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter import *


global files
files = {}

def load_data_from_file():
    if os.path.exists("user_files.json"):
        with open("user_files.json", "r") as file:
            return json.load(file)
    else:
        return {}

def register_user():
    with open("users.json", "r+") as file:
        data = json.load(file)
        username = reg_username.get()
        password = reg_password.get()
        user_exists = False

        for user in data["users"]:
            if user["username"] == username:
                user_exists = True
                break

        if user_exists:
            messagebox.showinfo("Error", "Username already exists")
        else:
            data["users"].append({"username": username, "password": password})
            file.seek(0)
            json.dump(data, file, indent=2)
            file.truncate()
            messagebox.showinfo("Success", "User registered successfully")
            reg_username.set("")
            reg_password.set("")

def login_user():
    with open("users.json", "r") as file:
        data = json.load(file)
        username = login_username.get()
        password = login_password.get()
        valid_user = False

        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                valid_user = True
                break

        if valid_user:
            messagebox.showinfo("Success", "Logged in successfully")
            login_username.set("")
            login_password.set("")
            root.destroy()
            main_notepad(username)
        else:
            messagebox.showinfo("Error", "Invalid username or password")

# def main_notepad(username):
#     def new_file(username):
#         file_name = simpledialog.askstring("New File", "Enter file name:")
#         if file_name:
#             files[username].append(file_name)
#             update_file_list(username)
#             text_area.delete("1.0", tk.END)

#     def delete_file(username):
#         selected_file = file_list.get(tk.ACTIVE)
#         if selected_file:
#             files[username].remove(selected_file)
#             update_file_list(username)

#     def save_file(username):
#         selected_file = file_list.get(tk.ACTIVE)
#         if selected_file:
#             content = text_area.get("1.0", tk.END)
#             with open(f"{username}_{selected_file}.txt", "w") as file:
#                 file.write(content)
#             messagebox.showinfo("Success", "File saved successfully.")

#     def load_file(username):
#         selected_file = file_list.get(tk.ACTIVE)
#         if selected_file:
#             text_area.delete("1.0", tk.END)
#             with open(f"{username}_{selected_file}.txt", "r") as file:
#                 content = file.read()
#             text_area.insert(tk.END, content)

#     def save_file_as(username):
#         file_path = filedialog.asksaveasfilename(defaultextension=".txt")
#         if file_path:
#             content = text_area.get("1.0", tk.END)
#             with open(file_path, "w") as file:
#                 file.write(content)
#             messagebox.showinfo("Success", "File saved successfully.")



def main_notepad(username):
    files = load_data_from_file()
    if username not in files:
        files[username] = {}
    notepad_window(username)

    # The rest of the function and helper functions go here
    
    def new_file(username):
        file_name = simpledialog.askstring("New File", "Enter file name:")
        if file_name:
            files[username][file_name] = ""
            update_file_list(username)
            text_area.delete("1.0", tk.END)

    def delete_file(username):
        selected_file = file_list.get(tk.ACTIVE)
        if selected_file:
            del files[username][selected_file]
            update_file_list(username)

    def save_file(username):
        selected_file = file_list.get(tk.ACTIVE)
        if selected_file:
            content = text_area.get("1.0", tk.END)
            files[username][selected_file] = content
            save_data_to_file()
            messagebox.showinfo("Success", "File saved successfully.")

    def load_file(username):
        selected_file = file_list.get(tk.ACTIVE)
        if selected_file:
            text_area.delete("1.0", tk.END)
            content = files[username][selected_file]
            text_area.insert(tk.END, content)

    def save_data_to_file():
        with open("user_files.json", "w") as file:
            json.dump(files, file, indent=2)

    def load_data_from_file():
        if os.path.exists("user_files.json"):
            with open("user_files.json", "r") as file:
                return json.load(file)
        else:
            return {}

    # global files
    # files = load_data_from_file()
    # if username not in files:
    #     files[username] = {}
    # notepad_window(username)




    def exit_application():
        root.destroy()

    def update_file_list(username):
        file_list.delete(0, tk.END)
        for file in files[username]:
            file_list.insert(tk.END, file)

    # def notepad_window(username):
    #     notepad = tk.Toplevel(root)
    #     notepad.title(f"{username}'s Notepad")
    def notepad_window(username):
        notepad = tk.Tk()  # Create a new Tk instance
        notepad.title(f"{username}'s Notepad")

        global file_list, text_area
        file_list = tk.Listbox(notepad)
        text_area = tk.Text(notepad)

        file_list.pack(side=tk.LEFT, fill=tk.Y)
        text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        menu = tk.Menu(notepad)
        notepad.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: new_file(username))
        file_menu.add_command(label="Delete", command=lambda: delete_file(username))
        file_menu.add_command(label="Save", command=lambda: save_file(username))
        file_menu.add_command(label="Load", command=lambda: load_file(username))
        # file_menu.add_command(label="Save As", command=lambda: save_file_as(username))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=exit_application)

        update_file_list(username)



    # global files
    # files = {}
    # files[username] = []
    # notepad_window(username)

def main_login():
    global root, login_username, login_password, reg_username, reg_password

    root = Tk()
    root.title("Login & Register")
    root.geometry("300x250")

    login_username = StringVar()
    login_password = StringVar()
    reg_username = StringVar()
    reg_password = StringVar()

    login_frame = Frame(root)
    login_frame.pack(side=LEFT, padx=10)

    Label(login_frame, text="Login", font=("Helvetica", 14, "bold")).pack()

    Label(login_frame, text="Username:").pack()
    Entry(login_frame, textvariable=login_username).pack()

    Label(login_frame, text="Password:").pack()
    Entry(login_frame, textvariable=login_password, show="*").pack()

    Button(login_frame, text="Login", command=login_user).pack(pady=5)

    register_frame = Frame(root)
    register_frame.pack(side=RIGHT, padx=10)

    Label(register_frame, text="Register", font=("Helvetica", 14, "bold")).pack()

    Label(register_frame, text="Username:").pack()
    Entry(register_frame, textvariable=reg_username).pack()

    Label(register_frame, text="Password:").pack()
    Entry(register_frame, textvariable=reg_password, show="*").pack()

    Button(register_frame, text="Register", command=register_user).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_login()

