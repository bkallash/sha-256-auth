import hashlib, os, binascii, getpass

DB_FILE = "users.txt"

def hash_pw(password: str, salt: str) -> str:
    # concatenate password + salt, then hash
    return hashlib.sha256((password + salt).encode()).hexdigest()

def user_exists(username):
    if not os.path.exists(DB_FILE):
        return False
    with open(DB_FILE) as f:
        return any(line.split(":")[0] == username for line in f)

def register():
    username = input("Choose username: ").strip()
    if not username or ":" in username:
        print("Invalid username."); return
    if user_exists(username):
        print("Username already taken."); return
    password = getpass.getpass("Choose password: ")
    salt = binascii.hexlify(os.urandom(16)).decode()
    with open(DB_FILE, "a") as f:
        f.write(f"{username}:{salt}:{hash_pw(password, salt)}\n")
    print("Registration successful.")

def login():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            for line in f:
                u, salt, stored = line.strip().split(":")
                if u == username:
                    if hash_pw(password, salt) == stored:
                        print("Login successful."); return
                    break
    print("Login failed: invalid username or password.")

while True:
    choice = input("\n1) Register  2) Login  3) Exit : ").strip()
    if choice == "1": register()
    elif choice == "2": login()
    elif choice == "3": break
