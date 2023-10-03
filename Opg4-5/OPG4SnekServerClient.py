import socket

serverHost = "127.0.0.1"
serverPort = 12003

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

try:
    while True:
        response = clientSocket.recv(1024).decode()
        print(response)

        if "Enter operation" in response:
            user_input = input().strip().lower()
            clientSocket.send(user_input.encode())
        elif "Enter number 1" in response or "Enter number 2" in response:
            user_input = input().strip().lower()
            clientSocket.send(user_input.encode())
        elif "Result" in response or "Invalid" in response:
            continue
        elif "Disconnected" in response:
            break

except ConnectionResetError:
    print("Server closed the connection.")

finally:
    clientSocket.close()





