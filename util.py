import hashlib
import os


def hash_password(password):
    salt = str(os.urandom(50))
    hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
    return hashed_password, salt


def hash_password_with_custom_salt(password, salt):
    hashed_password = hashlib.sha512((password + str(salt)).encode()).hexdigest()
    return hashed_password
