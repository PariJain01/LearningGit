from cryptography.fernet import Fernet
import os
import random
import string

# master key ;-
MASTER_PASSWORD = "Hello_world@123"

def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("key.key"):
        print("key not found generating the new one...")
        write_key()
    with open("key.key", 'rb') as key_file:
        key = key_file.read()
    return key


key = load_key()
fer = Fernet(key)

def add():
    name = input("Enter Account name: ")
    pwd = input("Enter Password: ")

    with open('password.txt', 'a') as file:
        file.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

def generate_fake_password():
    length = random.randint(8,12)
    fake_password = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
    return fake_password

def view(master_correct): 
    try:
        with open('password.txt', 'r') as file:
          for line in file.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            
            if master_correct:
                try:
                    decrypted_pwd = fer.decrypt(passw.encode()).decode()  # Decrypt password
                    print(f"User: {user} | Password: {decrypted_pwd}")
                except Exception:
                    print(f"User: {user} | Password: [Decryption Error]")
            else:
                print(f"User: {user} | Password: {generate_fake_password()}")

    except FileNotFoundError:
        print("No password stored yet")


def get_master_password():
    master_pwd = input("enter master password:  ")
    if master_pwd == MASTER_PASSWORD:
        print("Access Granted!")
        return True
    else:
        return False
    

while True:
    mode = input("would youn like to add password or view existing passwords or quit? (view/add/q): ").lower()
    if mode == "q":
        break

    if mode == "add":
        add()

    elif mode == "view":
        master_correct = get_master_password()
        view(master_correct)

    else:
        print("invalid mode")
        continue
