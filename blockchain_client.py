'''
author          :   Marcos Vinicius Sombra
version         :   0.1.1
python_version  :   3.6.7
description     :   Código para implementar uma interface de blockchain simples
'''

# import json
import binascii

import Crypto.Random as crip_random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5


class Transacao:
    '''
    Classe que implementa uma transação em uma blockchain
    Usuário que deseja enviar tokens para outro cria uma instância de Transacao
    '''

    def __init__(self, end_remetente, priv_remetente, end_destino, quantia):
        '''
        Inicia a transição com os atributos a seguir
        '''
        self.quantia = quantia
        self.endereco_remetente = end_remetente
        self.chave_privada_remetente = priv_remetente
        self.endereco_destino = end_destino

    def __str__(self):
        '''
        Retorna a string do dicionario contendo as informações da transação
        '''
        return str(self.get_dicionario())

    def get_dicionario(self):
        ''' Retorna um dicionario contendo as informações da transação '''
        return {'endereco_remetente': self.endereco_remetente,
                'endereco_destino': self.endereco_destino,
                'valor': self.quantia}

    def assinar_transacao(self):
        '''
        Remetente assina a transação, como forma de validação
        '''
        chave = RSA.importKey(binascii.unhexlify(self.chave_privada_remetente))
        assinante = PKCS1_v1_5.new(chave)
        h = SHA.new(self.__str__().encode('utf-8'))
        return binascii.hexlify(assinante.sign(h)).decode('ascii')


def carteira():
    '''
    Retorna uma carteira nova
    Retorna um dicionario com as chaves
    '''
    rand = crip_random.new().read
    chave_privada = RSA.generate(1024, rand)
    chave_publica = chave_privada.publickey()

    chave_privada = chave_privada.exportKey(format='DER')
    chave_publica = chave_publica.exportKey(format='DER')

    resp = {'chave_privada': binascii.hexlify(chave_privada).decode('ascii'),
            'chave_publica': binascii.hexlify(chave_publica).decode('ascii')
            }

    return resp


def criar_transacao(end_remetente, priv_remetente, end_destino, quantia):
    '''
    Retorna um dicionário com uma transação e uma assinatura
    '''
    t = Transacao(end_remetente, priv_remetente, end_destino, quantia)
    resp = {'transacao': t.get_dicionario, 'assinatura': t.assinar_transacao()}

    return resp
