import socket
import threading
import rsa

# Generate a public/private key pair for the server
(public_key, private_key) = rsa.newkeys(2048)


def handle_client(client_socket_1, client_socket_2):
    # Send the public key to the first client
    client_socket_1.send(public_key.save_pkcs1())

    # Receive the public key of the first client
    client_1_public_key_pem = client_socket_1.recv(4096).decode()
    client_1_public_key = rsa.PublicKey.load_pkcs1(client_1_public_key_pem.encode())

    # Send the public key to the second client
    client_socket_2.send(public_key.save_pkcs1())

    # Receive the public key of the second client
    client_2_public_key_pem = client_socket_2.recv(4096).decode()
    client_2_public_key = rsa.PublicKey.load_pkcs1(client_2_public_key_pem.encode())

    # Print information about the new clients
    print(f"New clients connected: {client_socket_1.getpeername()}, {client_socket_2.getpeername()}")

    while True:
        # Receive an encrypted message from the first client
        encrypted_message = client_socket_1.recv(4096)

        # Decrypt the message using the server's private key
        message = rsa.decrypt(encrypted_message, private_key).decode()

        # Print information about the received message
        print(f"Received message from client 1: {message}")

        # Encrypt the message using the second client's public key
        encrypted_message = rsa.encrypt(message.encode(), client_2_public_key)

        # Send the encrypted message to the second client
        client_socket_2.send(encrypted_message)

        # Receive an encrypted message from the second client
        encrypted_message = client_socket_2.recv(4096)

        # Decrypt the message using the server's private key
        message = rsa.decrypt(encrypted_message, private_key).decode()

        # Print information about the received message
        print(f"Received message from client 2: {message}")

        # Encrypt the message using the first client's public key
        encrypted_message = rsa.encrypt(message.encode(), client_1_public_key)

        # Send the encrypted message to the first client
        client_socket_1.send(encrypted_message)

    # Close the client sockets
    client_socket_1.close()
    client_socket_2.close()


def start_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 10000)
    print(f"Starting server on {server_address}")
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Wait for at least two clients to connect
    while True:
        print("Waiting for two clients to connect...")
        client_socket_1, address_1 = sock.accept()
        print(f"First client connected from {address_1}")
        client_socket_2, address_2 = sock.accept()
        print(f"Second client connected from {address_2}")

        # Create a new thread to handle the clients
        threading.Thread(target=handle_client, args=(client_socket_1, client_socket_2)).start()



start_server()
