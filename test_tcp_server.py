import socket
import asyncio

async def handle_client(client_socket, address):
    # Receive data from the client
    data = await loop.sock_recv(client_socket, 1024)
    message = data.decode()
    
    # Process the received data
    print(f"Received {message} from {address}")
    
    # Send a response back to the client
    response = f"Received {message}"
    response = "Response from server@"
    await loop.sock_sendall(client_socket, response.encode())
    
    # Close the client socket
    client_socket.close()

async def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to a specific address and port
    server_address = ('127.0.0.1', 8888)
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(5)
    print("Server is listening...")
    
    while True:
        # Accept a client connection
        client_socket, address = await loop.sock_accept(server_socket)
        
        # Handle the client in a separate coroutine
        asyncio.ensure_future(handle_client(client_socket, address))

# Create the event loop
loop = asyncio.get_event_loop()

# Start the server
asyncio.ensure_future(start_server())

# Run the event loop
loop.run_forever()