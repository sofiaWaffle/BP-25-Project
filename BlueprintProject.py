import sqlite3
import socket
import threading

# Step 1: Create SQLite database and add 7 username/password combinations
def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    users = [
        ("user1", "pass1"),
        ("user2", "pass2"),
        ("user3", "pass3"),
        ("user4", "pass4"),
        ("user5", "pass5"),
        ("user6", "pass6"),
        ("user7", "pass7"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", users)
    conn.commit()
    conn.close()

# Step 2: Handle client connections
def handle_client(client_socket):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        # Receive username and password from client
        data = client_socket.recv(1024).decode("utf-8")
        username, password = data.split(",")
        
        # Verify credentials
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            client_socket.send("Login successful".encode("utf-8"))
        else:
            client_socket.send("Invalid username or password".encode("utf-8"))
    except Exception as e:
        client_socket.send(f"Error: {str(e)}".encode("utf-8"))
    finally:
        client_socket.close()
        conn.close()

# Step 3: Start the server
def start_server():
    setup_database()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999...")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()