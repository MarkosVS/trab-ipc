'''
author          :   Marcos Vinicius Sombra
version         :   0.3.1
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
