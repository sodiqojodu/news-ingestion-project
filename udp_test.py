import socket, json

msg = {
    "title": "Breaking News",
    "content": "FastAPI UDP server works!",
    "timestamp": "2025-03-29T21:30:00Z",
    "source": "TerminalTest",
    "type": "udp"
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(msg).encode(), ("localhost", 9999))
