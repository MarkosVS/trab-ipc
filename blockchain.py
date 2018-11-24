'''
author          :   Marcos Vinicius Sombra
version         :   0.1
python_version  :   3.6.7
description     :   Código para implementar umablockchain simples
'''

from uuid import uuid4

from time import time


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
        bloco = {'num_bloco': len(self.chain) + 1,
                 'timestamp': time(),
                 'transacoes': self.transacoes,
                 'nonce': nonce,
                 'hash_anterior': hash_anterior}
        return bloco
