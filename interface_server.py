from threading import Thread
from blockchain import Blockchain

import socket
import pickle

fim_programa = False
nodes = []
chains = []


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


def recuperar_blockchain(porta):
    for i in range(len(chains)):
        if(chains[i][0] == porta):
            return i


def server(porta):
    nodes.append('localhost:{}'.format(porta))
    print(nodes)
    bc = Blockchain()
    corrente = pickle.load(open('blockchain.pkl', 'rb'))
    bc.corrente = corrente
    chains.append([porta, bc])
    index = recuperar_blockchain(porta)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', porta))
    server.listen(10)

    while(True):
        nova_corrente = pickle.load(open('blockchain.pkl', 'rb'))
        if(len(bc.corrente) < len(nova_corrente)):
            bc.corrente = nova_corrente

        if(len(nodes) > len(bc.nodes)):
            for node in nodes:
                bc.registrar_node(node)
            # att blockchain
            chains[index][1] = bc

        print(bc.nodes)

        conn, client = server.accept()

        while(True):
            try:
                msg = conn.recv(1024 * 10)
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
        chains[index][1] = bc

        if(fim_programa):
            break


def menu_minerar():
    print('Digite um node:')
    while(True):
        try:
            # 'localhost:{}'.format(porta)
            r = 'localhost:{}'
            resp = input()
            r.format(resp)
        except ValueError:
            r = -1
        finally:
            if(r in nodes):
                return resp
            print('Node não existe')


def minerar(node):
    bc = recuperar_blockchain(node)
    ultimo_bloco = bc.corrente[-1]
    nonce = bc.proof_of_work()

    hash_anterior = bc.get_hash(ultimo_bloco)
    bloco = bc.criar_bloco(nonce, hash_anterior)
    print(bc.get_hash(bloco))

    pickle.dump(bc.corrente, open('blockchain.pkl', 'wb'))


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
            node = menu_minerar()
            minerar(node)
        else:
            print('Serviço encerrado')
            break


if(__name__ == '__main__'):
    m = Thread(target=main)
    m.start()
    m.join()
    fim_programa = True
