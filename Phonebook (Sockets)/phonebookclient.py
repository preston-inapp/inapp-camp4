import socket

def client():
    host = socket.gethostbyname('DESKTOP-DH4N9T0')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, 12345))
    msg = input("COMMAND > ")
    while msg.lower().strip() != 'exit':
        client_socket.send(msg.encode())
        data = client_socket.recv(1024).decode()
        print("Response from Server:\n ", str(data))
        msg = input("Enter MSG:")
    client_socket.close()

if __name__ == "__main__":
    client()