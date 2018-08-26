# -*- coding: utf-8 -*-

__filename__ = 'server.py'
__author__ = 'CatswordsToken Shadow'
__copyright__ = 'Copyright 2018, CatswordsToken (token.catswords.com)'
__credits__ = ['CWDS', 'GNH']
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Go Namhyeon'
__email__ = 'gnh1201@gmail.com'
__status__ = 'Prototype'

from flask import Flask, jsonify, request
import json
from textwrap import dedent
from uuid import uuid4

from blockchain import Blockchain
from addressUtils import addressUtils
from paymentUtils import paymentUtils

app = Flask(__name__)

#node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()
paymentUtils = paymentUtils()
addressUtils = addressUtils()

node_identifier = addressUtils.generate_address()
sender_address = addressUtils.generate_address()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)

    # payment last block fee
    last_fee = blockchain.get_last_block_fee()

    payment_is_available = paymentUtils.is_available()
    if(payment_is_available == True):
        payment_id = paymentUtils.pay(block_fee)
        payment_destination_address = paymentUtils.get_destination_address()
        if paymentUtils.check_payment_id(payment_id):
            blockchain.new_transaction(
                sender=sender_address,
                recipient=node_identifier,
                amount=last_fee,
                data={
                    'payment_id' : payment_id,
                    'previous_hash': previous_hash,
                    'destination_address': payment_destination_address,
                    'comment': 'previous block paid by CatswordsToken(CWDS)'
                }
            )
        else:
           payment_is_available = False

    # if not payment available
    if payment_is_available == False:
        blockchain.new_transaction(
            sender=sender_address,
            recipient=node_identifier,
            amount=last_fee,
        )

        print('[Notice] ==== Notice from CatswordsToken(CWDS) ====')
        print('[Notice] If you want certificate block, get some CatswordsToken(CWDS) and pay this.')
        print('[Notice] http://token.catswords.com')
        print('[Notice] ==== Thank you ====')

    # create new block
    block = blockchain.new_block(proof, previous_hash)

    # make response
    response = {
        'message': 'new block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount', 'comment']
    if not all(k in values for k in required):
        return 'missing values', 400

    data = {
        'comment': values['comment']
    }

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], data)

    response = {'message': 'Transaction will be added to Block {0}'.format(index)}

    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200

@app.route('/address/new', methods=['GET'])
def new_address():
    addressUtils.generate_address()
    response = addressUtils.export_data()

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
