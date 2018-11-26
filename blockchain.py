'''
author          :   Marcos Vinicius Sombra
version         :   0.5
python_version  :   3.6.7
description     :   Código para implementar uma blockchain simples
'''

import requests
import binascii
from uuid import uuid4
from urllib.parse import urlparse

from hashlib import sha256
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from collections import OrderedDict

from time import time

DIFICULDADE = 4
MINERADOR = 'Blockchain'


class Blockchain:
    '''
    Classe que representa a Blockchain em si
    '''

    def __init__(self):
        '''
        Instancia uma Blockchain com os atributos a seguir:
        '''
        self.transacoes = []  # transações "pendentes"
        self.corrente = []  # lista de blocos adicionados
        self.nodes = set()
        self.id_node = str(uuid4()).replace('-', '')
        self.criar_bloco(0, '00')

    def __str__(self):
        '''
        Retorna uma string representando a blockchain
        '''
        msg = 'Blocos:\n'
        for bloco in self.corrente:
            msg += str(bloco) + '\n'
        return 'Blockchain:\n' + msg

    def registrar_node(self, url):
        '''
        Adiciona um novo node na lista de nodes
        '''
        parse_url = urlparse(url)

        if(parse_url.netloc):
            self.nodes.add(parse_url.netloc)
        elif parse_url.path:
            # aceita URL fora do padrão 192.168.0.1:5000.
            self.nodes.add(parse_url.path)
        else:
            raise ValueError('URL Inválida')

    def verificar_assinatura(self, remetente, assinatura, transacao):
        '''
        Verifica se a assinatura de uma transação está correta
        '''
        # traduz o endereço do remetente em uma chave publica
        chave_publica = RSA.importKey(binascii.unhexlify(remetente))
        # objeto para verificar
        verificador = PKCS1_v1_5.new(chave_publica)
        # hash da transação
        h = SHA.new(str(transacao).encode('utf-8'))
        # 'traduz' a assinatura
        assinatura = binascii.unhexlify(assinatura)

        # verifica se a assinatura é válida e retorna
        return verificador.verify(h, assinatura)

    def enviar_transacao(self, remetente, destino, quantia, assinatura):
        '''
        Adiciona uma transação à lista de transações
        '''
        # dicionário da transação
        t = OrderedDict({'endereco_remetente': self.endereco_remetente,
                         'endereco_destino': self.endereco_destino,
                         'valor': self.quantia})

        # caso a própria blockchain envie o token
        # i.e., seja uma recompensa de mineração
        # adiciona na lista
        if(remetente == MINERADOR):
            self.transacoes.append(t)
            return len(self.corrente) + 1
        # caso seja uma transação comum
        else:
            # verificação da assinatura
            verificacao = self.verificar_assinatura(remetente, assinatura, t)
            # caso seja válida, adiciona na lista
            if(verificacao):
                self.transacoes.append(t)
                return len(self.corrente) + 1
            # caso não seja, retorna false
            else:
                return False

    def criar_bloco(self, nonce, hash_anterior):
        '''
        Cria um bloco novo e adiciona-o na blockchain
        '''
        # dicionario do bloco
        bloco = {'num_bloco': len(self.corrente) + 1,
                 'timestamp': time(),
                 'transacoes': self.transacoes,
                 'nonce': nonce,
                 'hash_anterior': hash_anterior}

        # reseta a lista de transações pendentes
        self.transacoes = []
        # adiciona o bloco na blockchain
        self.corrente.append(bloco)
        # retorna o bloco
        return bloco

    def get_hash(self, bloco):
        ''' Retorna a hash de um bloco '''
        s = str(bloco).encode()
        return sha256(s).hexdigest()

    def proof_of_work(self):
        '''
        Algoritmo de prova de trabalho, garantindo maior segurança à rede
        '''
        # pega o ultimo bloco e sua hash
        ultimo_bloco = self.corrente[-1]
        ultimo_hash = self.get_hash(ultimo_bloco)

        # inicia o nonce como 0
        nonce = 0
        # enquando não resolver o problema, incrementa o nonce
        while(not self.prova_valida(self.transacoes, ultimo_hash, nonce)):
            nonce += 1

        return nonce

    def prova_valida(self, transacoes, ultimo_hash, nonce, dif=DIFICULDADE):
        '''
        Valida uma prova de trabalho
        '''

        # gera um hash palpite
        palpite = (str(transacoes) + str(ultimo_hash) + str(nonce)).encode()
        palpite = sha256(palpite).hexdigest()

        # retorna se o palpite começa com n zeros
        # n = dificuldade
        return palpite[:dif] == '0' * dif

    def blockchain_valida(self, corrente):
        '''
        Checa se a blockchain é válida
        '''

        # percorre os blocos (em pares)
        bloco_anterior = corrente[0]
        i = 1

        while(i < len(corrente)):
            bloco = corrente[i]

            # checa se a hash está correta
            if(bloco['hash_anterior'] != self.get_hash(bloco_anterior)):
                return False

            # checa se a prova de trabalho é correta

            # lista de transações (exceto a última)
            # ultima é recompensa de mineração
            tr_list = bloco['transacoes'][:-1]
            # elementos de cada transação
            trel = ['endereco_remetente', 'endereco_destino', 'valor']
            # lista de transações
            tr_list = [OrderedDict((k, tr[k]) for k in trel) for tr in tr_list]
            # hash do bloco anterior
            hash_anterior = bloco['hash_anterior']
            nonce = bloco['nonce']
            dif = DIFICULDADE

            if(not self.prova_valida(tr_list, hash_anterior, nonce, dif)):
                return False

            # atualiza os blocos
            bloco_anterior = bloco
            i += 1

        # retorna verdadeiro
        return True

    def resolver_conflitos(self):
        '''
        Resolve conflitos entre os nós da blockchain
        Substitui a nossa por uma maior
        '''
        vizinhos = self.nodes
        nova_blockchain = None

        max_tamanho = len(self.corrente)

        # percorre os nodes da blockchain e, caso encontre uma blockchain
        # maior e válida, substitui
        for node in vizinhos:
            print('http://' + node + '/chain')
            r = requests.get('http://' + node + '/chain')

            if(r.status_code == 200):
                tamanho = r.json()['length']
                corrente = r.json()['chain']

                if(tamanho > max_tamanho and self.blockchain_valida(corrente)):
                    nova_blockchain = corrente
                    max_tamanho = tamanho

        # sai do for aqui
        if(nova_blockchain):
            self.corrente = nova_blockchain
            return True
        return False
