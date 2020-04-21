import random


chars = '+-/*!&$?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generator_password(length_password):
    password = ''
    for i in range(length_password):
        password += random.choice(chars)
    return password

