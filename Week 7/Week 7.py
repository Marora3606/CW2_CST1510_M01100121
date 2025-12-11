# auth.py
# Week 7 - Secure Authentication System (CST1510)
# Implements: password hashing (bcrypt), registration, login, validation, simple menu

import bcrypt
import os
import re

USER_DATA_FILE = "users.txt"


# ---------------------------
# Core security functions
# ---------------------------
def hash_password(plain_text_password):
    """
    Hash a plaintext password using bcrypt (with automatic salt).
    Returns the hashed password as a UTF-8 string.
    """
    if not isinstance(plain_text_password, str):
        raise TypeError("password must be a string")
    pw_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()               # automatically generates a random salt
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode("utf-8")         # store as text


def verify_password(plain_text_password, hashed_password):
    """
    Verify a plaintext password against a stored bcrypt hash (string form).
    Returns True if match, False otherwise.
    """
    if not isinstance(plain_text_password, str) or not isinstance(hashed_password, str):
        return False
    try:
        pw_bytes = plain_text_password.encode("utf-8")
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        return False


# ---------------------------
# File helpers & user functions
# ---------------------------
def _ensure_user_file_exists():
    """Create the user data file if it does not exist."""
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            pass  # create empty file


def user_exists(username):
    """
    Return True if username exists in users.txt, False otherwise.
    Handles missing file gracefully.
    """
    if not isinstance(username, str) or username.strip() == "":
        return False
    _ensure_user_file_exists()
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format: username,hashed_password
            parts = line.split(",", 1)
            if len(parts) >= 1 and parts[0] == username:
                return True
    return False


def register_user(username, password):
    """
    Register a new user if username doesn't exist.
    Returns (True, message) on success, (False, message) on failure.
    """
    if user_exists(username):
        return False, f"Error: Username '{username}' already exists."

    # Hash the password and append to file
    hashed = hash_password(password)
    _ensure_user_file_exists()
    with open(USER_DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{hashed}\n")
    return True, f"Success: User '{username}' registered successfully!"


def login_user(username, password):
    """
    Authenticate username and password against the file.
    Returns (True, message) if successful, (False, message) otherwise.
    """
    if not user_exists(username):
        return False, "Error: Username not found."

    # Search for the username and verify password
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",", 1)
            if len(parts) < 2:
                continue
            stored_username, stored_hash = parts[0], parts[1]
            if stored_username == username:
                if verify_password(password, stored_hash):
                    return True, f"Success: Welcome, {username}!"
                else:
                    return False, "Error: Invalid password."
    # should not reach here if user_exists returned True, but safe fallback:
    return False, "Error: Username not found."


# ---------------------------
# Input validation helpers
# ---------------------------
def validate_username(username):
    """
    Validate username format.
    Criteria (example): 3-20 characters, only letters, numbers, underscore.
    Returns (is_valid, error_message)
    """
    if not isinstance(username, str) or username.strip() == "":
        return False, "Username cannot be empty."
    username = username.strip()
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters long."
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can only contain letters, numbers and underscore (_)."
    return True, ""


def validate_password(password):
    """
    Validate password strength.
    Criteria (example): 6-50 characters, must include at least one letter and one digit.
    Returns (is_valid, error_message)
    """
    if not isinstance(password, str):
        return False, "Password must be a string."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password must be no more than 50 characters long."
    # require at least one letter and one digit
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    return True, ""


# ---------------------------
# CLI menu / main program
# ---------------------------
def display_menu():
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def main():
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        try:
            display_menu()
            choice = input("\nPlease select an option (1-3): ").strip()
            if choice == '1':
                # Registration flow
                print("\n--- USER REGISTRATION ---")
                username = input("Enter a username: ").strip()
                is_valid, error_msg = validate_username(username)
                if not is_valid:
                    print(f"Error: {error_msg}")
                    continue

                password = input("Enter a password: ").strip()
                is_valid, error_msg = validate_password(password)
                if not is_valid:
                    print(f"Error: {error_msg}")
                    continue

                password_confirm = input("Confirm password: ").strip()
                if password != password_confirm:
                    print("Error: Passwords do not match.")
                    continue

                success, msg = register_user(username, password)
                print(msg)

            elif choice == '2':
                # Login flow
                print("\n--- USER LOGIN ---")
                username = input("Enter your username: ").strip()
                password = input("Enter your password: ").strip()
                success, msg = login_user(username, password)
                print(msg)
                if success:
                    # Optional: simple logged-in interaction
                    input("\nPress Enter to return to the main menu...")

            elif choice == '3':
                print("\nThank you for using the authentication system. Exiting...")
                break

            else:
                print("\nError: Invalid option. Please select 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break


# Allow running as a script
if __name__ == "__main__":
    main()