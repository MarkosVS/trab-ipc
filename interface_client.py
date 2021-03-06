from blockchain_client import (carteira, criar_transacao)
from threading import Thread
from collections import deque
import socket
import pickle

fim_programa = False
transacoes = deque([])


def menu_inicial():
    print('Selecione uma operação:')
    print('(1) Criar Carteira')
    print('(2) Realizar transação')
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


def menu_transacao():
    with open('carteiras/info.txt', 'r') as f:
        qtd = int(f.readlines()[0]) + 1

    print('Digite o número da carteira do remetente:')
    while(True):
        try:
            rem = int(input())
        except ValueError:
            rem = -1
        finally:
            if(rem >= 1 and rem <= qtd):
                rem = str(rem)
                break
            print('Resposta inválida')

    print('Digite o número da carteira do destinatário:')
    while(True):
        try:
            dest = int(input())
        except ValueError:
            dest = -1
        finally:
            if(dest >= 1 and dest <= qtd and dest != rem):
                dest = str(dest)
                break
            print('Resposta inválida')

    rem = pickle.load(open('carteiras/carteira{}.pkl'.format(rem), 'rb'))
    dest = pickle.load(open('carteiras/carteira{}.pkl'.format(dest), 'rb'))

    print('Digite a quantia:')
    while(True):
        try:
            qt = float(input())
        except ValueError:
            qt = -1
        finally:
            if(qt > 0):
                break
            print('Resposta inválida')
    return criar_transacao(rem['chave_publica'], rem['chave_privada'],
                           dest['chave_publica'], qt)


def nome_carteira_nova():
    with open('carteiras/info.txt', 'r') as f:
        qtd = str(int(f.readlines()[0]) + 1)
    with open('carteiras/info.txt', 'w') as f:
        f.write(qtd)

    return 'carteiras/carteira' + qtd + '.pkl'


def client():
    while(True):
        while(len(transacoes) == 0):
            if(fim_programa):
                break

        t, porta = transacoes.popleft()
        t = pickle.dumps(t)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con = ('localhost', porta)
        client.connect(con)
        print('Client conectado\nURL: {}\nPorta: {}'.format(con[0], con[1]))
        client.send(t)
        # encerra o client
        client.close()


def main():
    print('Client-side Blockchain Service')
    print('Validação: Proof-of-work')
    while(True):
        r = menu_inicial()
        if(r == 1):
            nova = carteira()
            nome = nome_carteira_nova()
            pickle.dump(nova, open(nome, 'wb'))
            print('Chave pública:\n{}'.format(nova['chave_publica']))
            print('Chave privada:\n{}'.format(nova['chave_privada']))
        elif(r == 2):
            transacao = menu_transacao()
            tupla = (transacao, 5000)
            transacoes.append(tupla)
        else:
            print('Serviço encerrado')
            break


if(__name__ == '__main__'):
    s = Thread(target=client)
    s.start()
    main = Thread(target=main)
    main.start()
    main.join()
    fim_programa = True
