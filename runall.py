import subprocess
import time
import threading
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import socket
import os

# --- Start server in a separate thread ---
def start_server():
    subprocess.Popen(["python3", "server+setup.py"])

# --- GUI login logic ---
def login():

    valid_username = "user"
    valid_password = "1234"

    username = username_entry.get()
    password = password_entry.get()

    if username == valid_username and password == valid_password:
        messagebox.showinfo("Login Success", "You have successfully logged in!")

    else:
        messagebox.showerror("Error", "Invalid username or password!")    
        
        '''try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 9999))
        client.send(f"{username},{password}".encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        client.close()

        ttk.messagebox.showinfo("Server Response", response)
    except Exception as e:
        ttk.messagebox.showerror("Error", str(e))'''

# --- Run everything ---
def main():
    # Start the server
    threading.Thread(target=start_server, daemon=True).start()
    
    # Wait a sec to ensure server is listening
    time.sleep(1)

    # Start GUI
    global username_entry, password_entry
    root = ttk.Window(themename="cerculean")
    root.title("Login Client")

    root.geometry("400x420")
    root.resizable(False, False)

    content = ttk.Frame(root, padding=20)
    content.pack(expand=True)

    icon_path = "snorlax.jpeg"  # or snorlax.png if you're using a converted PNG
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        img = img.resize((80, 80))
        icon_img = ImageTk.PhotoImage(img)
        icon_label = ttk.Label(content, image=icon_img)
        icon_label.image = icon_img
        icon_label.grid(row=0, column=0, pady=(0, 10))

    # Username label
    ttk.Label(content, text="Username:").grid(row=1, column=0, sticky="w", padx=5)
    username_entry = ttk.Entry(content, width=20)
    username_entry.grid(row=2, column=0, pady=(0, 15), padx=5)

    # Password label
    ttk.Label(content, text="Password:").grid(row=3, column=0, sticky="w", padx=5)
    password_entry = ttk.Entry(content, show="*", width=20)
    password_entry.grid(row=4, column=0, pady=(0, 20), padx=5)

    # Login Button
    ttk.Button(content, text="Login", bootstyle=SUCCESS, command=login, width=5).grid(row=5, column=0, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()


