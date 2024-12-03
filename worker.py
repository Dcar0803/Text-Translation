from deep_translator import GoogleTranslator
import asyncio
from functools import lru_cache

@lru_cache(maxsize=100)
def cache_translate(text, target_language):
    return GoogleTranslator(target=target_language).translate(text)

async def handle_worker(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Worker connected by server at {addr}")

    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode()
            text, target_language = message.split('|')

            try:
                translation = cache_translate(text, target_language)
                response = translation
                print(f"Translated: '{text}' to '{translation}' in '{target_language}'")
            except Exception as e:
                response = f"Error during translation: {e}"
                print(f"Error: {e}")

            writer.write(response.encode())
            await writer.drain()
        
        except Exception as e:
            print(f"Worker error: {e}")
            break

    writer.close()
    await writer.wait_closed()

def start_worker(port):
    async def run_worker():
        print(f"Starting worker agent on port {port}...")
        server = await asyncio.start_server(handle_worker, '192.168.1.19', port)
        print(f"Worker agent running on port {port}")

        async with server:
            await server.serve_forever()

    asyncio.run(run_worker())
