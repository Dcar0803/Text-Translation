import asyncio
from multiprocessing import Process
from worker import start_worker

LANGUAGES = {
    'server1': ['es', 'fr'],
    'server2': ['de', 'it'],
    'server3': ['pt', 'ru'],
    'server4': ['ja', 'ko'],
    'server5': ['el', 'ht'],
    'server6': ['hi', 'vi'],
}

SERVER_IP = '192.168.1.19'  # Replace with your local or public IP

async def delegate_to_worker(text, target_language, worker_port):
    try:
        reader, writer = await asyncio.open_connection(SERVER_IP, worker_port)
        writer.write(f"{text}|{target_language}".encode())
        await writer.drain()

        data = await reader.read(1024)
        translation = data.decode()
        writer.close()
        await writer.wait_closed()
        return translation
    except Exception as e:
        return f"Error communicating with worker: {e}"

async def handle_client(reader, writer, languages, server_name, worker_port):
    addr = writer.get_extra_info('peername')
    print(f"[{server_name}] Client connected from {addr}")

    data = await reader.read(1024)
    message = data.decode()
    text, target_language = message.split('|')

    if target_language in languages:
        translation = await delegate_to_worker(text, target_language, worker_port)
        writer.write(translation.encode())
        print(f"[{server_name}] Translated text for {target_language}: {translation}")
    else:
        writer.write(f"Language {target_language} not supported".encode())
        print(f"[{server_name}] Language {target_language} not supported")

    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print(f"[{server_name}] Client disconnected from {addr}")

async def main_server(languages, port, worker_port, server_name):
    print(f"[{server_name}] Starting server on {SERVER_IP}:{port}...")

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, languages, server_name, worker_port),
        SERVER_IP, port
    )
    print(f"[{server_name}] Server running on {SERVER_IP}:{port}")

    async with server:
        await server.serve_forever()

def start_server(languages, port, worker_port, server_name):
    asyncio.run(main_server(languages, port, worker_port, server_name))

def launch_servers():
    processes = []

    server_configs = [
        (LANGUAGES['server1'], 5001, 7001, 'server1'),
        (LANGUAGES['server2'], 5002, 7002, 'server2'),
        (LANGUAGES['server3'], 5003, 7003, 'server3'),
        (LANGUAGES['server4'], 5004, 7004, 'server4'),
        (LANGUAGES['server5'], 5005, 7005, 'server5'),
        (LANGUAGES['server6'], 5006, 7006, 'server6'),
    ]

    for languages, server_port, worker_port, server_name in server_configs:
        server_process = Process(target=start_server, args=(languages, server_port, worker_port, server_name))
        server_process.start()
        processes.append(server_process)

        worker_process = Process(target=start_worker, args=(worker_port,))
        worker_process.start()
        processes.append(worker_process)

    for process in processes:
        process.join()

if __name__ == "__main__":
    launch_servers()
