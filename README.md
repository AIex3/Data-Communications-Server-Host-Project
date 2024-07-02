# Data-Communications-Server-Host-Project
This project takes two hosts and connects them to a server. When connected they can send encrypted messages to each other using RSA encryption. 


Server:

This code defines a function named handle_client which takes two client sockets as input arguments. The purpose of this function is to enable secure communication between two clients through an intermediate server.

Here is how the function works:
The server sends its own public key to the first client using client_socket_1.send(public_key.save_pkcs1()). The public key is used for encryption and decryption of messages.
The first client sends its public key to the server using client_1_public_key_pem = client_socket_1.recv(4096).decode(). The server then loads the public key of the first client using rsa.PublicKey.load_pkcs1(client_1_public_key_pem.encode()). This public key will be used by the server to encrypt messages sent to the first client.
Steps 1 and 2 are repeated for the second client using client_socket_2.send(public_key.save_pkcs1()) and rsa.PublicKey.load_pkcs1(client_2_public_key_pem.encode()), respectively.
The server then enters an infinite loop where it waits for messages from the first client and then forwards them to the second client, and vice versa.
When a message is received from the first client, it is decrypted using the server's private key using rsa.decrypt(encrypted_message, private_key).decode(). The decrypted message is then printed to the console using print(f"Received message from client 1: {message}").
The message is then encrypted using the public key of the second client using rsa.encrypt(message.encode(), client_2_public_key). The encrypted message is then sent to the second client using client_socket_2.send(encrypted_message).
Steps 5 and 6 are repeated for messages from the second client, but this time the message is encrypted using the public key of the first client using rsa.encrypt(message.encode(), client_1_public_key) and then sent to the first client using client_socket_1.send(encrypted_message).
The function continues to loop until either client disconnects from the server. When a client disconnects, the function exits the loop and closes both client sockets using client_socket_1.close() and client_socket_2.close().


This code defines a function named start_server that sets up a server to handle secure communication between two clients. Here is how the function works:

First, it creates a TCP/IP socket using socket.socket(socket.AF_INET, socket.SOCK_STREAM).
It binds the socket to a specific address and port using sock.bind(server_address). In this example, the server is bound to the local host (localhost) on port 10000.
The server starts listening for incoming connections using sock.listen(1). The argument passed to listen() is the maximum number of queued connections that can be waiting for a server to accept them. In this case, the server is only listening for one connection at a time.
The server then enters an infinite loop where it waits for at least two clients to connect using sock.accept(). accept() waits until a client connects to the server and then returns a new socket object and the address of the client. The first client's socket and address are stored in client_socket_1 and address_1, respectively. Similarly, the second client's socket and address are stored in client_socket_2 and address_2.
When two clients have connected, the server creates a new thread to handle them using threading.Thread(target=handle_client, args=(client_socket_1, client_socket_2)).start(). target is set to the handle_client function, which will be executed in a separate thread. args is a tuple containing the two client sockets, which will be passed to the handle_client function as arguments.
The server then continues to wait for at least two clients to connect and repeats the loop.
This function sets up the basic structure of a server that can handle multiple clients using threads. The actual communication between the clients is handled by the handle_client function.

Client:


This code connects a client to a server using sockets and implements RSA encryption to securely exchange messages between the client and another connected client.

First, the server address and port are defined, and a socket is created to connect to the server. Then, a new RSA key pair is generated for this client using the newkeys() function from the rsa module.

The client's public key is sent to the server using the send() method of the socket, and the public key of the other connected client is received from the server using the recv() method of the socket.

Then, the program enters a loop to send and receive messages between the two connected clients. The user is prompted to enter a message to send, and this message is encrypted using the other client's public key with the encrypt() function from the rsa module.

The encrypted message is then sent to the server using the send() method of the socket. The client receives an encrypted message from the server using the recv() method of the socket, which is then decrypted using the client's private key with the decrypt() function from the rsa module.

The decrypted message is printed to the console, and the loop continues until the program is terminated.



