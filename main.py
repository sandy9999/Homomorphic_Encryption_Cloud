from Crypto.Util.number import *
import random
import pymysql
import json
import base64

def encrypt(N):
    with open('public_key.txt') as p:
        variables = json.load(p)
    intpart, decimalpart = str(N).split(".")
    intpart = int(intpart)
    decimalpart = int(decimalpart)
    P0 = variables["P0"]
    P1 = variables["P1"]
    T1 = random.getrandbits(4)
    T2 = random.getrandbits(4)
    P2 = (T1*P1)%P0
    C1 = (intpart+T2*P2)%P0
    C2 = (decimalpart+T2*P2)%P0
    C1 = base64.b64encode(long_to_bytes(C1)).decode('utf-8')
    C2 = base64.b64encode(long_to_bytes(C2)).decode('utf-8')
    C = C1 + "." + C2
    return C

def decrypt(C):
    with open('private_key.txt') as p:
        variables = json.load(p)
    J = variables["J"]
    K = variables["K"]
    C1, C2 = C.split('.')
    C1 = bytes_to_long(base64.b64decode(C1.encode('utf-8')))
    C2 = bytes_to_long(base64.b64decode(C2.encode('utf-8')))
    intpart = (C1%J)%K
    decimalpart = float("." + str((C2%J)%K))
    N = intpart + decimalpart
    return N

if __name__=='__main__':
    db = pymysql.connect("localhost","phpmyadmin","","nw_proj")
    cursor = db.cursor()
    print("Enter your choice")
    print("1. Add new data to database")
    print("2. View marks")
    print("3. Exit")
    while(1):
        choice = int(input())
        if choice == 1:
            print("Enter name")
            name = input()
            print("Enter science marks")
            science = float(input())
            print("Enter math marks")
            math = float(input())
            print("Enter english marks")
            english = float(input())
            cursor.execute("INSERT INTO marks (name,science,math,english) VALUES ('%s','%s','%s','%s')" % (name,str(encrypt(science)),str(encrypt(math)),str(encrypt(english))))
            db.commit()
        elif choice == 2:
            print("Enter name whose marks you want to view")
            name = input()
            numofrows = cursor.execute("SELECT * FROM marks where name = '%s' " % (name))
            if not numofrows == 0:
                data = cursor.fetchone()
                print("Name: " + str(data[0]))
                print("Science marks: " + str(decrypt(data[1])))
                print("Math marks: " + str(decrypt(data[2])))
                print("English marks: " + str(decrypt(data[3])))
                db.commit()
            else:
                print("The name doesn't exist in the database")
        elif choice == 3:
            db.close()
            break