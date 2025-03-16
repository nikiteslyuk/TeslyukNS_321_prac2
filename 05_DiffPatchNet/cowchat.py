import asyncio
import cowsay
import shlex

clients = {}
cow_names = set(cowsay.list_cows())


async def chat(reader, writer):
    writer.write(b"CowChat\n")
    await writer.drain()

    cow_name = None
    queue = asyncio.Queue()

    async def send_messages():
        while True:
            message = await queue.get()
            writer.write(message.encode() + b"\n")
            await writer.drain()

            writer.write(b">> ")
            await writer.drain()

    send_task = asyncio.create_task(send_messages())

    while not reader.at_eof():
        writer.write(b">> ")
        await writer.drain()

        data = await reader.readline()
        if not data:
            break

        message = data.decode().strip()
        command = shlex.split(message)

        if not command:
            continue

        cmd, *args = command

        if cmd == "login":
            if cow_name:
                writer.write(b"You are already logged in!\n")
            elif args and args[0] in cow_names and args[0] not in clients:
                cow_name = args[0]
                clients[cow_name] = queue
                writer.write(f"Logged in as {cow_name}.\n".encode())
            else:
                writer.write(b"Invalid or taken cow name!\n")
            await writer.drain()

        elif cmd == "who":
            writer.write(f"Active cows: {', '.join(clients.keys())}\n".encode())
            await writer.drain()

        elif cmd == "cows":
            writer.write(
                f"Available cow names: {', '.join(cow_names - clients.keys())}\n".encode()
            )
            await writer.drain()

        elif cmd == "say" and cow_name:
            if len(args) < 2:
                writer.write(b"Usage: say <cow_name> <message>\n")
            elif args[0] in clients:
                msg = "\n" + cowsay.cowsay(" ".join(args[1:]), cow=cow_name)
                await clients[args[0]].put(msg)
            else:
                writer.write(b"No such cow online.\n")
            await writer.drain()

        elif cmd == "yield" and cow_name:
            msg = "\n" + cowsay.cowsay(" ".join(args), cow=cow_name)
            for name, q in clients.items():
                if name != cow_name:
                    await q.put(msg)

        elif cmd == "quit":
            break

        else:
            writer.write(b"Unknown command or not logged in.\n")
            await writer.drain()

        # writer.write(b">> ")
        # await writer.drain()

    if cow_name:
        del clients[cow_name]
    send_task.cancel()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
