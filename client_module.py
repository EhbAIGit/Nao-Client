import socket
import threading

def create_client_connection(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    return client_socket

def listen_for_messages(client_socket, message_callback):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            ascii_message = message.encode('ascii', 'ignore')
            if message:
                print("Received from server", ascii_message)
                message_callback(ascii_message)
                send_message(client_socket, "success")  # Send success response
            else:
                break  # If an empty string is received, close the connection
        except socket.error as e:
            print ("Socket error: ", e)
            break  # The connection was reset by the server
        except Exception as e:
            print ("An error occurred: ", e)
            break  # The socket was closed, so break out of the loop

def send_message(client_socket, message):
    client_socket.send(message.encode())

def close_connection(client_socket):
    client_socket.close()

def start_listening(client_socket, message_callback):
    thread = threading.Thread(target=listen_for_messages, args=(client_socket, message_callback))
    thread.daemon = True  # Daemon threads will shut down when the main program exits
    thread.start()
