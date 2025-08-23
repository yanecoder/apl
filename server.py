from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

@socketio.on('register')
def handle_register(data):
    client_id = data['id']
    clients[client_id] = request.sid
    print(f"Client registered: {client_id} -> {request.sid}")
    emit('log', {'msg': f'Registered {client_id}'}, room=request.sid)

@socketio.on('signal')
def handle_signal(data):
    to_id = data['to']
    from_id = data.get('from', '')
    payload = data.get('payload', {})
    target_sid = clients.get(to_id)
    if target_sid:
        emit('signal', {'from': from_id, 'payload': payload, 'type': data['type']}, room=target_sid)
        print(f"Signal {data['type']} from {from_id} -> {to_id}")
    else:
        print(f"Target {to_id} not found")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for client_id, s in list(clients.items()):
        if s == sid:
            print(f"Client disconnected: {client_id}")
            del clients[client_id]
            break

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8443)
