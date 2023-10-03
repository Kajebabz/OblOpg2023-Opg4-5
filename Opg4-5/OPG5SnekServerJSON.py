import socket
import threading
import json
import random

def handle_client(connectionSocket, addr):
    print(f"{addr} is Connected")
    connectionSocket.send("\nWelcome to the SnekServer!".encode())

    KeepConnected = True    
    while KeepConnected:
        try:
            request_data = connectionSocket.recv(1024).decode()
            if not request_data:
                print(f"{addr} is Disconnected")
                break 

            request = json.loads(request_data)
            action = request.get("action", "").strip().lower()

            if action == "quit":
                KeepConnected = False
            elif action in ['random', 'add', 'sub', 'mul', 'div']:
                num1 = request.get("num1", 0)
                num2 = request.get("num2", 0)

                if action == 'random':
                    if num1 > num2:
                        response = {"error": "Invalid range. Must provide the lowest number first"}
                    else:
                        result = random.randint(int(num1), int(num2))
                        response = {"result": result}
                elif action == 'add':
                    result = num1 + num2
                    response = {"result": result}
                elif action == 'sub':
                    result = num1 - num2
                    response = {"result": result}
                elif action == 'mul':
                    result = num1 * num2
                    response = {"result": result}
                elif action == 'div':
                    result = num1 / num2
                    response = {"result": result}
                else:
                    response = {"error": "Invalid operation. Please try again."}

                connectionSocket.send(json.dumps(response).encode())
            else:
                response = {"error": "Invalid operation. Please try again."}
                connectionSocket.send(json.dumps(response).encode())
        except json.JSONDecodeError:
            response = {"error": "Invalid JSON request. Please try again."}
            connectionSocket.send(json.dumps(response).encode())
        except ValueError:
            response = {"error": "Invalid input. Must provide a number."}
            connectionSocket.send(json.dumps(response).encode())
        except ConnectionResetError:
            print(f"{addr} is Disconnected due to a connection error")
            break

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