'''
author          :   Marcos Vinicius Sombra
version         :   0.2
python_version  :   3.6.7
description     :   Código para implementar uma blockchain simples
'''

from uuid import uuid4
from hashlib import sha256

from time import time

DIFICULDADE = 4


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

    def criar_bloco(self, nonce, hash_anterior):
        '''
        Cria um bloco novo e adiciona-o na blockchain
        '''
        bloco = {'num_bloco': len(self.corrente) + 1,
                 'timestamp': time(),
                 'transacoes': self.transacoes,
                 'nonce': nonce,
                 'hash_anterior': hash_anterior}

        self.transacoes = []
        self.corrente.append(bloco)
        return bloco

    def get_hash(self, bloco):
        ''' Retorna a hash de um bloco '''
        s = str(bloco).encode()
        return sha256(s).hexdigest()

    def proof_of_work(self):
        '''
        Algoritmo de prova de trabalho, garantindo maior segurança à rede
        '''
        ultimo_bloco = self.corrente[-1]
        ultimo_hash = self.get_hash(ultimo_bloco)

        nonce = 0
        while(not self.prova_valida(self.transacoes, ultimo_hash, nonce)):
            nonce += 1

        return nonce

    def prova_valida(self, transacoes, ultimo_hash, nonce, dif=DIFICULDADE):
        '''
        Valida uma prova de trabalho
        '''
        palpite = (str(transacoes) + str(ultimo_hash) + str(nonce)).encode()
        palpite = sha256(palpite).hexdigest()
        return palpite[:dif] == '0' * dif
