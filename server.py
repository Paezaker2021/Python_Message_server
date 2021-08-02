import threading
import socket
host = 'localhost'
port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients = []
aliases = []

print('서버 구동 시작...', host,'주소의', port,'포트에서 성공적으로 시작했습니다')

def broadcast(message):
    for client in clients:
        client.send(message)


#개인 연결을 관리하는 함수

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} 님이 방을 떠나셨습니다.'.encode
            ('utf-8'))
            aliases.remove(alias)
            break

#개인 연결을 받기 위한 메인 함수

def receive():
    while True:

        client, address = server.accept()
        print(f'{str(address)}와(과) 연결되었습니다.')
        client.send('alias?'.encode('UTF-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'{alias}님이 접속하셨습니다.'.encode('UTF-8'))

        client.send('메인 서버와 성공적으로 연결되었습니다.'.encode('UTF-8'))
        thread = threading.Thread(target=handle_client, args=(client, ))
        thread.start()


if __name__ =='__main__':
    receive()
