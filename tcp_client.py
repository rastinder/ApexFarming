import asyncio


class TCPClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.reader = None
        self.writer = None

    async def connect(self):
        while True:
            try:
                self.reader, self.writer = await asyncio.open_connection(self.server_ip, 8888)
                print('Connected to server')
                break
            except (ConnectionRefusedError, ConnectionResetError,OSError):
                print('Connection failed. Retrying in 5 seconds...')
                await asyncio.sleep(5)

    async def send_message(self, message):
        message_bytes = message.encode() + b'@'
        self.writer.write(message_bytes)
        #await self.writer.drain()

    async def receive_message(self):
        response_bytes = await self.reader.readuntil(b'@')
        response_str = response_bytes.decode().rstrip('@')
        return response_str

    async def run(self, message):
        await self.connect()

        await self.send_message(message)

        response = await self.receive_message()
        print('Received response:', response)

        self.writer.close()
        await self.writer.wait_closed()


# Example usage
async def main():
    server_ip = '127.0.0.1'  # Replace with the actual server IP
    client = TCPClient(server_ip)

    message_to_send = "Hello, server!"
    await client.run(message_to_send)


#asyncio.run(main())
