import subprocess
import time
import threading
import tkinter as tk
from tkinter import messagebox
import socket

# --- Start server in a separate thread ---
def start_server():
    subprocess.Popen(["python3", "server+setup.py"])

# --- GUI login logic ---
def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 9999))
        client.send(f"{username},{password}".encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        client.close()

        messagebox.showinfo("Server Response", response)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Run everything ---
def main():
    # Start the server
    threading.Thread(target=start_server, daemon=True).start()
    
    # Wait a sec to ensure server is listening
    time.sleep(1)

    # Start GUI
    global username_entry, password_entry
    root = tk.Tk()
    root.title("Login Client")

    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
