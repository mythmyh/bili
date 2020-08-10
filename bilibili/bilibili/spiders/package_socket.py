import socket
import os

using = ' '


def register1(use_for='for socket transparent'):
    def register_port(func):
        def writing_port(*args):
            result = func(*args)
            if not os.path.exists('/home/mayinghao/port.json'):
                os.mknod('/home/mayinghao/port.json')

            with open('/home/mayinghao/port.json', 'a+') as f:
                end = f.tell()
                f.seek(0)
                lines = f.readlines()
                f.seek(end)
                print(lines)
                print([x for x in lines if x.startswith(str(args[0]))])
                if [x for x in lines if x.startswith(str(args[0]))]:
                    pass
                else:
                    f.write(str(args[0])+':' + use_for+'\n')

            return result
        return writing_port
    return register_port


def receive_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(5)
    s1, address = s.accept()
    while True:
        get_str = s1.recv(2000).decode('utf-8')
        yield get_str
        try:
            s1.send('hello,world'.encode('utf-8'))
        except BrokenPipeError:

            s1.close()
            break


def send_socket(port, *args):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = port
    client.connect((host, port))
    index = 0
    while True:
        client.send(str(args[index]).encode('utf-8'))
        d = client.recv(2000).decode('utf-8')
        index += 1
        yield d
        if index == 2:
            break


