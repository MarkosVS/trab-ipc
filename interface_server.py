from threading import Thread
from blockchain import Blockchain

import socket
import pickle

fim_programa = False
nodes = []


def menu_inicial():
    print('Selecione uma operação:')
    print('(1) Criar nó')
    print('(2) Minerar')
    print('(3) Encerrar')
    respostas = (1, 2, 3)
    while(True):
        try:
            resp = int(input())
        except ValueError:
            resp = -1
        finally:
            if(resp in respostas):
                return resp
            print('Resposta inválida')


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

        while(True):
            try:
                msg = conn.recv(1024)
                msg = pickle.loads(msg)
                t = msg['transacao']
                rem = t['endereco_remetente']
                dest = t['endereco_destino']
                qt = t['valor']
                ass = msg['assinatura']
            except EOFError:
                continue

            if(msg):
                break

        bc.enviar_transacao(rem, dest, qt, ass)

        if(fim_programa):
            break


def main():
    print('Server-side Blockchain Service')
    print('Validação: Proof-of-work')
    porta = 5000
    while(True):
        r = menu_inicial()
        if(r == 1):
            print('Nó criado. Porta: {}'.format(porta))
            s = Thread(target=server, args=(porta, ))
            s.start()
            porta += 1
        elif(r == 2):
            pass
        else:
            print('Serviço encerrado')
            break


if(__name__ == '__main__'):
    m = Thread(target=main)
    m.start()
    m.join()
    fim_programa = True
