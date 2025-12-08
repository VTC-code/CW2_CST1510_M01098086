import bcrypt
import os
 
# Function to hash passwords
def hash_password(plain_text_password):
    """Hash a password for storing."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')  # Convert bytes to string for storage
 
# Function to verify passwords
def verify_password(plain_text_password, hashed_password):
    """Verify a stored password against one provided by user."""
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
 
# Function to register users
def register_user(username, password):
    """Register a new user by saving username and hashed password."""
    hashed = hash_password(password)
   
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed}\n")
   
    print(f"User '{username}' registered successfully!")
 
# Function to login users
def login_user(username, password):
    """Check login credentials."""
    if not os.path.exists("users.txt"):
        return False
   
    with open("users.txt", "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(",", 1)
            if stored_user == username:
                return verify_password(password, stored_hash)
    return False  # Username not found

if __name__ == "__main__":
    
    print("\n--- TESTING HASH FUNCTION ---")
    test_password = "SecurePassword123"
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}")
    print(f"Hash length: {len(hashed)} characters")
 
    print("\nTesting with correct password:",
          verify_password(test_password, hashed))
    print("Testing with incorrect password:",
          verify_password("WrongPassword", hashed))

    print("\n--- REGISTERING USER ---")
    register_user("Farhan", "mypassword")
 
    print("\n--- LOGIN ATTEMPTS ---")
    if login_user("Farhan", "mypassword"):
        print("Login successful!")
    else:
        print("Login failed.")
 
    if login_user("Farhan", "wrongpassword"):
        print("Login successful!")
    else:
        print("Login failed.")
