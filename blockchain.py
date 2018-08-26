# -*- coding: utf-8 -*-

__filename__ = 'blockchain.py'
__author__ = 'CatswordsToken Shadow'
__copyright__ = 'Copyright 2018, CatswordsToken'
__credits__ = ['CWDS', 'GNH', 'YHY']
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Go Namhyeon'
__email__ = 'gnh1201@gmail.com'
__status__ = 'Prototype'

import hashlib
import json
from time import time
from uuid import uuid4
import pickle

class Blockchain(object):

    def __init__(self):
        self.filename_fullchain = 'fullchain.dat'
        self.chain = self.read_fullchain()
        self.current_transactions = []
        self.transaction_fee = 0.1
        self.block_fee = 1.0

        if len(self.chain) == 0:
            self.new_block(previous_hash=1, proof=100) # genesis block

    def write_fullchain(self):
        wrote = False;

        try:
            with open(self.filename_fullchain, 'wb') as fp:
                pickle.dump(self.chain, fp)
                wrote = True
        except IOError as e:
            print "Unable to open fullchain file"

        return wrote

    def read_fullchain(self):
        fullchain = []

        try:
            with open(self.filename_fullchain, 'rb') as fp:
                fullchain = pickle.load(fp)
        except IOError as e:
             fullchain = []
             print "Will be write new fullchain data"

        return fullchain

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.chain.append(block)
        self.current_transactions = []
        self.write_fullchain()

        return block

    def new_transaction(self, sender, recipient, amount, data={}):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'data': data
        })

        return self.last_block['index'] + 1

    def get_block_fee(self, block):
        fee = self.block_fee + (len(block['transactions']) * self.transaction_fee)
        return fee

    def get_last_block_fee(self):
        return self.get_block_fee(self.last_block)

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof * proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
