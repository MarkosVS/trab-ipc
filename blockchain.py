'''
author          :   Marcos Vinicius Sombra
version         :   0.3
python_version  :   3.6.7
description     :   Código para implementar uma blockchain simples
'''

import binascii
from uuid import uuid4

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

    def verificar_assinatura(self, remetente, assinatura, transacao):
        '''
        Verifica se a assinatura de uma transação está correta
        '''
        chave_publica = RSA.importKey(binascii.unhexlify(remetente))
        verificador = PKCS1_v1_5.new(chave_publica)
        h = SHA.new(str(transacao).encode('utf-8'))
        assinatura = binascii.unhexlify(assinatura)

        return verificador.verify(h, assinatura)

    def enviar_transacao(self, remetente, destino, quantia, assinatura):
        '''
        Adiciona uma transação à lista de transações
        '''
        t = OrderedDict({'endereco_remetente': self.endereco_remetente,
                         'endereco_destino': self.endereco_destino,
                         'valor': self.quantia})

        if(remetente == MINERADOR):
            self.transacoes.append(t)
            return len(self.corrente) + 1
        else:
            verificacao = self.verificar_assinatura(remetente, assinatura, t)
            if(verificacao):
                self.transacoes.append(t)
                return len(self.corrente) + 1
            else:
                return False

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
