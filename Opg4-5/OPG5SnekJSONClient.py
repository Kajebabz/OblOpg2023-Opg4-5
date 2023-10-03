import socket
import json

serverHost = "127.0.0.1"
serverPort = 12003

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

print(clientSocket.recv(1024).decode())

while True:
    action = input("Enter operation (random/add/sub/mul/div/quit): ").strip().lower()

    if action == "quit":
        break

    if action in ['random', 'add', 'sub', 'mul', 'div']:
        try:
            num1 = float(input("Enter number 1: "))
            num2 = float(input("Enter number 2: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

        request = {"action": action, "num1": num1, "num2": num2}

        clientSocket.send(json.dumps(request).encode())

        response = clientSocket.recv(1024).decode()
        response_data = json.loads(response)

        if "result" in response_data:
            print(f"Result: {response_data['result']}")
        elif "error" in response_data:
            print(f"Server Error: {response_data['error']}")

clientSocket.close()
