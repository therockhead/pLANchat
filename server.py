import socket
import threading
import pickle

clients = []

def handle_client(client, addr):
    print(f"[CONNECTED] {addr}")
    
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break

            # 🔥 Extract message
            msg = pickle.loads(data)
            username = msg.get("username", "Unknown")

            print(f"[RECEIVED from {username}]")

            # ✅ Broadcast to others
            broadcast(data, client)

        except Exception as e:
            print(f"[ERROR] {addr} - {e}")
            break

    clients.remove(client)
    client.close()
    print(f"[DISCONNECTED] {addr}")

def broadcast(data, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(data)
            except:
                pass

# def start_server(host='0.0.0.0', port=5555):
# def start_server(host='127.0.0.1', port=5555):
def start_server(host='0.0.0.0', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER RUNNING] on {host}:{port}")

    while True:
        client, addr = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
