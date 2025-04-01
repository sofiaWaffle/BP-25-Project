import socket

# Step 1: Connect to the server and send username/password
def start_client(username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))  # Connect to the server
    # Format credentials as "username,password"
    client.send(f"{username},{password}".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")  # Receive server response
    print(response)  # Print the response
    client.close()

if __name__ == "__main__":
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    start_client(username, password)