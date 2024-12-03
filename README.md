# Translation Application

This project is a distributed computing translation application. It demonstrates multiprocessing, multithreading, interprocess communication, distributed computing over networked machines, and internode communication. The application allows text to be translated into multiple languages through a network of worker servers.

## Features

- **Multiprocessing:** Workers handle translations using separate processes.
- **Multithreading:** Enables concurrent handling of translation requests.
- **Interprocess Communication:** Communication between the Flask web interface and the worker servers.
- **Distributed Computing:** Worker servers handle translation tasks across multiple machines.
- **Internode Communication:** Translation requests are routed between the main application and worker nodes via sockets.

## Requirements
- Python 3.10 or later
- Flask for the web interface
- Socket programming for communication
- Deep_Translation Library
- Local network setup for distributed worker servers

## Setup Instructions

### Step 1: Update IP Addresses
Before running the application, update the IP addresses to match your network setup:
1. Open `app.py` and `server.py` on the same machine.
2. Replace the placeholder IP address `192.168.1.51` with the actual IP address of the machine running the worker servers.

For example:
```python
SERVERS = {
    'es': ('192.168.1.10', 5001),
    'fr': ('192.168.1.10', 5001),
    # Update other entries similarly
}

3. Access the application in your web browser at: http://<host-ip>:5000. 
Note:Replace <host-ip> with the IP address of the machine running app.py.
For example: The server.py and app.py runs on the 192.168.1.19 ip address.
## http://192.168.1.19:5000

4. All the machines need to be connected to the same network. For example: Open a web browser on any device connected to the network (e.g., VSU-GUEST).
