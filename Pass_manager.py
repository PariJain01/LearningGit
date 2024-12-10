from cryptography.fernet import Fernet
import os
import random
import string

# Constant for the master password
MASTER_PASSWORD = "Hello_world@123"

def write_key():
    """Generates and writes a new encryption key to a file."""
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)

def load_key():
    """Loads the encryption key from the file. If it doesn't exist, generates a new one."""
    if not os.path.exists("key.key"):
        print("Key not found. Generating a new one...")
        write_key()
    with open("key.key", 'rb') as key_file:
        key = key_file.read()
    return key

# Load the encryption key
key = load_key()
fer = Fernet(key)

def add():
    """Adds a new password entry to the password file."""
    name = input("Enter account name: ")
    pwd = input("Enter password: ")

    with open('password.txt', 'a', encoding='utf-8') as file:
        file.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

def generate_fake_password():
    """Generates a random fake password."""
    length = random.randint(8, 12)
    fake_password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return fake_password

def view(master_correct):
    """Views stored passwords, either decrypted or fake, based on the master password."""
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                
                if master_correct:
                    try:
                        decrypted_pwd = fer.decrypt(passw.encode()).decode()  # Decrypt password
                        print(f"User: {user} | Password: {decrypted_pwd}")
                    except Exception as e:
                        print(f"User: {user} | Password: [Decryption Error: {e}]")
                else:
                    print(f"User: {user} | Password: {generate_fake_password()}")

    except FileNotFoundError:
        print("No password stored yet")

def get_master_password():
    """Prompts the user for the master password and validates it."""
    master_pwd = input("Enter master password: ")
    if master_pwd == MASTER_PASSWORD:
        print("Access granted!")
        return True
    else:
        print("Access denied!")
        return False

def main():
    """Main loop to add, view, or quit password management."""
    while True:
        mode = input("Would you like to add a password, view existing passwords, or quit? (view/add/q): ").lower()
        if mode == "q":
            break

        if mode == "add":
            add()

        elif mode == "view":
            master_correct = get_master_password()
            if master_correct:
                view(master_correct)

        else:
            print("Invalid mode. Please try again.")

if __name__ == "__main__":
    main()
