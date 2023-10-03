import socket
import threading
import random

def handle_client(connectionSocket, addr):
    print(f"{addr} is Connected")
    connectionSocket.send("Welcome to the SnekServer!".encode())

    KeepConnected = True    
    while KeepConnected:
        connectionSocket.send("\nEnter operation (random/add/sub/mul/div/quit): ".encode())
        action = connectionSocket.recv(1024).decode()

        if not action:
            print(f"{addr} is Disconnected")
            break 

        action = action.strip().lower()

        if action == "quit":
            KeepConnected = False
            print(f"{addr} is Disconnected")
        elif action in ['random', 'add', 'sub', 'mul', 'div']:

            try:       
                connectionSocket.send("Enter number 1: ".encode())
                num1 = float(connectionSocket.recv(1024).decode())

                connectionSocket.send("Enter number 2: ".encode())
                num2 = float(connectionSocket.recv(1024).decode())

                result = None

                if action == 'random':
                    if num1 > num2:
                        connectionSocket.send("Invalid range. Must provide the lowest number first".encode())
                    else:
                        result = random.randint(int(num1), int(num2))
                elif action == 'add':
                    result = num1 + num2
                elif action == 'sub':
                    result = num1 - num2
                elif action == 'mul':
                    result = num1 * num2
                elif action == 'div':
                    result = num1 / num2    

                if result is not None:
                    connectionSocket.send(f"Result: {result}\n".encode())
            except ValueError:
                response = "Invalid input. Must provide a number."
                connectionSocket.send(response.encode())
        else:
            connectionSocket.send("Invalid operation. Please try again.".encode())

    connectionSocket.close()

serverPort = 12003
serverHost = "127.0.0.1"

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen(5)

print("Server is ready to connect")

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()
    except KeyboardInterrupt:
        print("Server closed.")
        break
