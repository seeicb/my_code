from pyDes import *
import base64
k = des("DESCRYPT", CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
def DesEncrypt(str):
    str=str.encode(encoding="utf-8")#转换bytes
    EncryptStr = k.encrypt(str)
    return EncryptStr

def DesDecrypt(str):
    DecryptStr = k.decrypt(str)

    return DecryptStr
def fileEncrypt(str):
    EncryptStr = k.encrypt(str)
    return EncryptStr
