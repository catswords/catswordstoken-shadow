# -*- coding: utf-8 -*-

__filename__ = 'addressUtils.py'
__author__ = 'CatswordsToken Shadow'
__copyright__ = 'Copyright 2018, CatswordsToken'
__credits__ = ['CWDS', 'GNH']
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Go Namhyeon'
__email__ = 'gnh1201@gmail.com'
__status__ = 'Prototype'

import hashlib
import base58
from Crypto import Random
from Crypto.PublicKey import RSA

class addressUtils(object):
    def __init__(self):
        self.data = {}

    def export_data(self):
        return self.data

    def generate_keys(self):
        # RSA modulus length must be a multiple of 256 and >= 1024
        modulus_length = 256*4 # use larger value in production
        privatekey = RSA.generate(modulus_length, Random.new().read)
        publickey = privatekey.publickey()
        return privatekey, publickey

    def generate_address(self):
        s_priv, s_pub = self.generate_keys()

        address = None

        # (1) SHA256 hash
        h01 = hashlib.sha256(s_pub.exportKey())
        print('(1) SHA256 hash : ', h01.digest())

        # (2) RIPEMD160 hash
        r01 = hashlib.new('ripemd160')
        r01.update(h01.digest())
        line01 = r01.digest()
        print('(2) RIPEMD160 hash : ', line01)

        # (3) Prefix version byte
        line01 = b'\x00' + line01
        print('(3) Prefix version byte : ', line01)

        # (4) After Double hash, Calc checksum 4 Byte
        h02 = hashlib.sha256(line01)
        h03 = hashlib.sha256(h02.digest())
        check_sum = h03.digest()[0:4]
        print('(4) After Double hash, Calc checksum 4 Byte : ', check_sum)

        # (5) Add checksum at th end of Step 3,
        # Then the 25 bytes binary Bitcoin address
        result = (line01 + check_sum)
        print('(5) Add checksum at th end of Step 3, : ', result)

        # (6) Base58check encoding
        address = base58.b58encode(result)
        print('(6) Base58check encoding :', address)

        # export to data
        self.data["address"] = address

        # return address
        return address
