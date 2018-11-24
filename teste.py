# imports
from datetime import datetime
from hashlib import sha256


class Block:
    def __init__(self, dado):
        self.index = 0
        self.dado = dado
        self.proximo = None
        self.nonce = 0
        self.hash_anterior = 0x0
        self.carimbo_temporal = datetime.now()

    def __str__(self):
        return "Index: " + str(self.index) + "\nHash: " + str(self.hash())

    def hash(self):
        h = sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.dado).encode('utf-8') +
            str(self.hash_anterior).encode('utf-8') +
            str(self.carimbo_temporal).encode('utf-8') +
            str(self.index).encode('utf-8')
        )

        return h.hexdigest()


class Blockchain:
    def __init__(self):
        self.ultimo = Block('Genesis')
        self.primeiro = self.ultimo
        self.max_nonce = 2 ** 32
        self.dificuldade = 4
        self.alvo = 2 ** (256 - self.dificuldade)

    def add(self, novo):
        novo.hash_anterior = self.ultimo.hash()
        novo.index = self.ultimo.index + 1
        self.ultimo.proximo = novo
        self.ultimo = self.ultimo.proximo

    def mine(self, bloco):
        for i in range(self.max_nonce):
            '''
            if(int(bloco.hash(), 16) <= self.alvo):
            '''
            if(bloco.hash().startswith('0' * self.dificuldade)):
                self.add(bloco)
                print(bloco)
                break
            else:
                bloco.nonce += 1


bc = Blockchain()
for i in range(10):
    bloco = Block('Bloco {}'.format(i))
    bc.mine(bloco)

while(bc.primeiro is not None):
    print(bc.primeiro)
    bc.primeiro = bc.primeiro.proximo
