from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import config

def generate_token(id):
    s = Serializer(config.SHARED_SECRET_KEY)
    token = s.dumps({'id': id})
    return token.decode('ascii')

def verify_token(token, secret_key=None):
    s = Serializer(secret_key if secret_key != None else config.SHARED_SECRET_KEY)
    try:
        s.loads(token)
    except SignatureExpired:
        print("Token expired")
        return False
    except BadSignature:
        print("Token does not exist")
        return False
    return True