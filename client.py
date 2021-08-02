import threading
import socket
from win10toast import ToastNotifier
import time

toaster = ToastNotifier()
            
print('\n사용 하시기 전에...\n\n이름은 5글자 이하로, 내용은 20자 내용으로 입력해주세요.\n채팅을 치신 후 버그 방지를 위해 5초간 입력이 제한됩니다.\n')
alias = input('이름을 입력해주세요 : ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.219.109', 9999))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'alias?':
                client.send(alias.encode('utf-8'))
            else:
                notification(message)
                print(message)

        except:
            toaster.show_toast("오류 : 서버와 연결되지 않습니다.",
                   "사용자의 네트워크 문제나 호스트 서버의 문제일 수도 있습니다. 관리자에게 문의하세요.",
                   icon_path='information.ico',
                   duration=100,
                   threaded=True)
            print('오류')
            client.close()
            break


def client_send():
    while True:
        message = f'{alias} : {input("-")}'
        client.send(message.encode('utf-8'))
        time.sleep(5)

def notification(text):
    toaster.show_toast("알림이 도착했습니다.",
                   text,
                   icon_path='information.ico',
                   threaded=True)

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()

