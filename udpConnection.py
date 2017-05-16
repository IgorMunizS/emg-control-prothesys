import socket,time


def connect(msg):
    host = '127.0.0.1'
    port = 5000

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.connect((host, port))

    mySocket.send(msg.encode())
    msg_r = msg + '_r'
    print(msg_r)
    time.sleep(2)
    mySocket.send(msg_r.encode())


def aux_coleta(msg):
    host = '127.0.0.1'
    port = 5000

    mov = 0
    while mov != 5:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.connect((host, port))

        msg_sound = 'sound'
        msg_sound_r = 'sound_r'

        mySocket.send(msg_sound.encode())
        time.sleep(0.5)

        mySocket.send(msg.encode())
        msg_r = msg + '_r'
        print(msg_r)
        time.sleep(5)
        mySocket.send(msg_sound_r.encode())
        time.sleep(0.5)
        mySocket.send(msg_r.encode())
        time.sleep(2)


        mov += 1
    # 0.5 s pra começar depois 5 + 2*0.5s de coleta mais 2s de descanso


def msgRT(msg):
    host = '127.0.0.1'
    port = 5000

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.connect((host, port))

    mySocket.send(msg.encode())

