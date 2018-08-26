# -*- coding: utf-8 -*-

__filename__ = 'paymentUtils.py'
__author__ = 'CatswordsToken Shadow'
__copyright__ = 'Copyright 2018, CatswordsToken'
__credits__ = ['CWDS', 'GNH']
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Go Namhyeon'
__email__ = 'gnh1201@gmail.com'
__status__ = 'Prototype'

import requests
import json
import os
import binascii
from requests import RequestException, HTTPError, ConnectionError

class paymentUtils(object):
    def __init__(self):
        self.url = "http://localhost:18082/json_rpc"
        self.destination_address = ""

        self.headers = {
            "content-type": "application/json"
        }
        self.set_destination_address("cwdsGEF6VVqWw8K1i8MnqpFqrzKwXnnhr19Bmy26g7xd3FJkgFg3tHR4Kk2Ke3oGo2353FHGDPuStFU4sLTHvyAp54EUZ4KvND");

    def is_available(self):
        flag = True
        try:
            requests.get(self.url)
        except (RequestException, HTTPError, ConnectionError) as e:
            flag = False
        return flag

    def set_url(self, url):
        self.url = url

    def set_destination_address(self, address):
        self.destination_address = address

    def get_destination_address(self):
        return self.destination_address

    def make_rpc_input(self, data):
        data.update({
            "jsonrpc": "2.0",
            "id": "0"
        })

        return data

    def pay(self, amount):
        int_amount = int(get_amount(amount))

        assert amount == float(get_money(str(int_amount))), "Amount conversion failed"

        recipents = [{
            "address": self.destination_address,
            "amount": int_amount
        }]

        mixin = 4
        payment_id = get_payment_id()

        rpc_input = make_rpc_input({
            "method": "transfer",
            "params": {
                "destinations": recipents,
                "mixin": mixin,
                "payment_id" : payment_id
            }
        })

        response = requests.post(
            self.url,
            data=json.dumps(rpc_input),
            headers=self.headers,
        )

        print("#payment_id: ", payment_id)

        return payment_id

    def get_amount(self, amount):
        dp_point = 12

        str_amount = str(amount)

        fraction_size = 0

        if '.' in str_amount:

            point_index = str_amount.index('.')

            fraction_size = len(str_amount) - point_index - 1

            while fraction_size < dp_point and '0' == str_amount[-1]:
                print(44)
                str_amount = str_amount[:-1]
                fraction_size = fraction_size - 1

            if dp_point < fraction_size:
                return False

            str_amount = str_amount[:point_index] + str_amount[point_index+1:]

        if not str_amount:
            return False

        if fraction_size < dp_point:
            str_amount = str_amount + '0'*(dp_point - fraction_size)

        return str_amount

    def get_money(self, amount):
        dp_point = 12

        s = amount

        if len(s) < dp_point + 1:
            s = '0' * (dp_point + 1 - len(s)) + s

        idx = len(s) - dp_point

        s = s[0:idx] + "." + s[idx:]

        return s

    def get_payment_id(self):
        random_32_bytes = os.urandom(32)
        payment_id = "".join(map(chr, binascii.hexlify(random_32_bytes)))

        return payment_id

    def get_payment_info(self, payment_id):
        rpc_input = make_rpc_input({
            "method": "get_payments",
            "params": {
                "payment_id": payment_id
            }
        })

        response = requests.post(
            self.url,
            data=json.dumps(rpc_input),
            headers=self.headers,
        )

        return response.json();

    def check_payment_id(self, payment_id):
        checked = False
        payment_info = self.get_payment_info(payment_id)

        payments = payment_info.result.payments
        while i < len(payments):
            if payment_id == payments[i].payment_id:
                checked = True
                break

        return checked
