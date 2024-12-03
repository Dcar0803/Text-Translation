import socket
import threading

SERVERS = {
    'es': ('192.168.1.19', 5001), 'fr': ('192.168.1.19', 5001),
    'de': ('192.168.1.19', 5002), 'it': ('192.168.1.19', 5002),
    'pt': ('192.168.1.19', 5003), 'ru': ('192.168.1.19', 5003),
    'ja': ('192.168.1.19', 5004), 'ko': ('192.168.1.19', 5004),
    'el': ('192.168.1.19', 5005), 'ht': ('192.168.1.19', 5005),
    'hi': ('192.168.1.19', 5006), 'vi': ('192.168.1.19', 5006),
}

def translate_request(text, target_language):
    server_address = SERVERS.get(target_language)
    if server_address:
        try:
            with socket.create_connection(server_address) as sock:
                sock.sendall(f"{text}|{target_language}".encode())
                data = sock.recv(1024)
                translation = data.decode()
                print(f"Translation to {target_language}: {translation}")
        except ConnectionRefusedError:
            print(f"Could not connect to server for language {target_language}")
    else:
        print(f"Server for language {target_language} not found")

def main():
    text = input("Enter the paragraph to translate: ")
    target_languages = list(SERVERS.keys())

    threads = []
    for lang in target_languages:
        thread = threading.Thread(target=translate_request, args=(text, lang))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
