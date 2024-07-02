import socket
import rsa

# Define the server's address and port
server_address = 'localhost'
server_port = 10000

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))

# Generate a new RSA key pair for this client
(public_key, private_key) = rsa.newkeys(512)

# Send the public key to the server
client_socket.send(public_key.save_pkcs1())

# Receive the public key of the other client
other_client_public_key_pem = client_socket.recv(4096).decode()
other_client_public_key = rsa.PublicKey.load_pkcs1(other_client_public_key_pem.encode())

# Loop to send messages to the other client
while True:
    # Get a message from the user
    message = input("Enter a message to send: ")

    # Encrypt the message using the other client's public key
    encrypted_message = rsa.encrypt(message.encode(), other_client_public_key)

    # Send the encrypted message to the server
    client_socket.send(encrypted_message)

    # Receive an encrypted message from the server
    encrypted_message = client_socket.recv(4096)

    # Decrypt the message using the client's private key
    message = rsa.decrypt(encrypted_message, private_key).decode()

    # Print the received message
    print(f"Received message: {message}")
