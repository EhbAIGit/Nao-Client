from client_module import create_client_connection, send_message, close_connection, start_listening
import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = create_client_connection(host, port)
    start_listening(client_socket, handle_received_message)  # Start the listener thread

    try:
        while True:
            # The main thread can perform other tasks or shut down on a command
            new_message = ''
            command = raw_input("Enter 'exit' to quit: ")
            if command.lower() == 'exit':
                break
    finally:
        close_connection(client_socket)

def handle_received_message(message):
    print("Received from server ", message)
    

if __name__ == '__main__':
    client_program()
