import random
import json

def generate_private_key():
    J = random.getrandbits(64)
    K = random.getrandbits(16)
    private_key_file = open('private_key.txt','w')
    private_key_file.write('{ "J": ' +  str(J) + ', "K": ' + str(K) + ' }')

def generate_public_key():
    D = random.getrandbits(256)
    F = random.getrandbits(256)
    K_ = random.getrandbits(4)
    with open('private_key.txt') as p:
        variables = json.load(p)
    J = variables["J"]
    K = variables["K"]
    P0 = J*D
    P1 = J*F + K*K_
    public_key_file = open('public_key.txt','w')
    public_key_file.write('{ "P0": ' +  str(P0) + ', "P1": ' + str(P1) + ' }')

if __name__=='__main__':
    generate_private_key()
    generate_public_key()