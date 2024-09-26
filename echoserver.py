import socket
import threading

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received message: {message}")
            response = "Server received your message: " + message
            client_socket.sendall(response.encode('utf-8'))
    except ConnectionError as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        server_socket.close()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345

    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            message = input("Enter your message: ")
            if message.lower() == 'exit':
                print("Closing connection.")
                break
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            response = data.decode('utf-8')
            print(f"Server response: {response}")

    except ConnectionError as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    mode = input("Enter 'server' to start the server or 'client' to start the client: ").strip().lower()
    if mode == 'server':
        start_server()
    elif mode == 'client':
        start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")