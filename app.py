from flask import Flask, request, render_template
import socket

app = Flask(__name__)

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
                return data.decode()
        except ConnectionRefusedError:
            return f"Error: Could not connect to server for language {target_language}"
    else:
        return f"Error: Server for language {target_language} not found"

@app.route('/', methods=['GET', 'POST'])
def index():
    translation = None
    error = None
    if request.method == 'POST':
        text = request.form.get('text')
        target_language = request.form.get('language')
        if text and target_language:
            translation = translate_request(text, target_language)
        else:
            error = "Please provide both text and a target language."
    return render_template('index.html', translation=translation, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
