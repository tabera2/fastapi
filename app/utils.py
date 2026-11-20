from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()

def hash(password: str):
    return password_hash.hash(password)


def verify(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)