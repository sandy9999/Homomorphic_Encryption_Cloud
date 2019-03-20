import random
import pymysql
import json

def encrypt(N):
    with open('public_key.txt') as p:
        variables = json.load(p)
    P0 = variables["P0"]
    P1 = variables["P1"]
    T1 = random.getrandbits(4)
    T2 = random.getrandbits(4)
    P2 = (T1*P1)%P0
    C = (N+T2*P2)%P0
    return C

def decrypt(C):
    with open('private_key.txt') as p:
        variables = json.load(p)
    J = variables["J"]
    K = variables["K"]
    N = (C%J)%K
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
            science = int(input())
            print("Enter math marks")
            math = int(input())
            print("Enter english marks")
            english = int(input())
            cursor.execute("INSERT INTO marks (name,science,math,english) VALUES ('%s','%s','%s','%s')" % (name,str(encrypt(science)),str(encrypt(math)),str(encrypt(english))))
            db.commit()
        elif choice == 2:
            print("Enter name whose marks you want to view")
            name = input()
            cursor.execute("SELECT * FROM marks where name = '%s' " % (name))
            data = cursor.fetchone()
            print("Name: " + str(data[0]))
            print("Science marks: " + str(decrypt(int(data[1]))))
            print("Math marks: " + str(decrypt(int(data[2]))))
            print("English marks: " + str(decrypt(int(data[3]))))
            db.commit()
        elif choice == 3:
            db.close()
            break