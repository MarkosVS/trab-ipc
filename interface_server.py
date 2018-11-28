from threading import Thread
from blockchain import Blockchain

import socket

fim_programa = False
nodes = []


def server(porta):
    bc = Blockchain()
    nodes.append('localhost:{}'.format(porta))
    for node in nodes:
        bc.registrar_node(node)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('localhost', porta))
    server.listen(10)

    while(True):
        conn, client = server.accept()
        if(fim_programa):
            break


def main():
    print('Server-side Blockchain Service')
    print('Validação: Proof-of-work')
    while(True):
        pass


if(__name__ == '__main__'):
    s = Thread(target=server)
    s.start()
    m = Thread(target=main)
    m.start()
    m.join()
    fim_programa = True
