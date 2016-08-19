# -- encoding: utf-8 --
__author__ = 'PD-002'

try:
    import simplejson as json
except:
    import json
import os
import rsa
import base64

pubkey_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "publickey.txt")
privkey_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "privatekey.txt")

class RsaServer:
    """
        rsa校验服务端校验方式
    """

    @classmethod
    def check(cls, sec_data, sign):
        pubkey = cls._loadkey(pubkey_path)
        try:
            my_sign = base64.b64decode(sign)
            if rsa.verify(sec_data, my_sign, pubkey):
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def _loadkey(filename):
        with open(filename) as fd:
            key_data = fd.read()
        return rsa.PublicKey.load_pkcs1(key_data)


class RsaClient:
    """
        rsa校验客户端数据处理方式
    """
    def __init__(self, data):
        self.data = data

    def create(self):
        my_sign = self._sign(self.data)
        self.data["sign_type"] = "RSA-1"
        self.data["sign"] = my_sign
        return self.data

    def _sign(self, data):
        privkey = self._loadkey(privkey_path)
        my_sign = rsa.sign(data["sec_data"], privkey, "SHA-1")
        return my_sign

    @staticmethod
    def _loadkey(filename):
        with open(filename) as fd:
            key_data = fd.read()
        return rsa.PrivateKey.load_pkcs1(key_data)

class RsaBulid:
    """
        生成rsa秘钥
    """
    def __init__(self):
        self.keysize = 512

    def build(self):
        (pubkey, privkey) = rsa.newkeys(self.keysize)
        self.save_to_file(pubkey_path, pubkey)
        self.save_to_file(privkey_path)

    @staticmethod
    def save_to_file(filename, content, format_name="PEM"):
        content = content.save_pkcs1(format=format_name)
        with open(filename, "w+") as fd:
            fd.write(content)

if __name__ == "__main__":
    # RsaBulid().build()
    # data = {"aa": 12, "bb": "", "cc": "dd"}
    data = {"sec_data": "X8zPj5mMdKq2w9J6p6J5yQ5kAjJv5kCc2mWgVzC3o4I0P5eM6MuLdL0XsOjFhCw9"}
    create_data = RsaClient(data).create()
    print "client_data: ", create_data
    # print "check: ", RsaServer.check(create_data)