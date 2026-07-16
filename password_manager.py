"""
password_manager.py

A simple, beginner-friendly command-line Password Manager.
Everything lives in this one file so you can read it top to bottom.

Run this file to start the program:
    python password_manager.py

All data is stored locally in passwords.json (created automatically
the first time you save an entry). Nothing is sent over the network.

NOTE FOR LEARNERS:
This project stores passwords in PLAIN TEXT for simplicity, so you can
focus on core Python concepts (functions, dictionaries, files, JSON,
loops, error handling). A production password manager would encrypt
this data — see the README for notes on how you could extend this.

File layout (all in this one file, top to bottom):
    1. Imports & constants
    2. Input helpers       -> get_yes_no, find_entry
    3. Data helpers        -> load_data, save_data
    4. Password helpers    -> generate_password, check_strength
    5. Display helpers     -> display_menu, print_entry
    6. Menu actions        -> add/view/search/update/delete/generate
    7. Main loop           -> ties everything together
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import json
import os
import random
import string

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# File where all password entries are stored (created in current directory).
DATA_FILE = "passwords.json"

# Characters allowed in generated passwords.
SYMBOLS = "!@#$%^&*()-_=+"

# Strength scoring thresholds.
STRONG_THRESHOLD = 5
MEDIUM_THRESHOLD = 3

# Password length limits for generation.
MIN_LENGTH = 4
MAX_LENGTH = 64
DEFAULT_LENGTH = 12

# ---------------------------------------------------------------------------
# Input Helpers — validate and sanitize user input
# ---------------------------------------------------------------------------


def get_yes_no(prompt):
    """
    Keep asking until the user enters 'y' or 'n'.

    Args:
        prompt (str): The question to display.

    Returns:
        str: 'y' or 'n' (lowercase).
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("⚠  Please enter 'y' or 'n'.")


def find_entry(data, name):
    """
    Find an entry by name using case-insensitive matching.

    Args:
        data (dict): The password dictionary.
        name (str): The website/app name to search for.

    Returns:
        str or None: The matching key if found, otherwise None.
    """
    for key in data:
        if key.lower() == name.lower():
            return key
    return None


# ---------------------------------------------------------------------------
# Data Helpers — read/write passwords.json
# ---------------------------------------------------------------------------


def load_data():
    """
    Load password data from the JSON file.

    Returns:
        dict: A dictionary of all saved entries, e.g.
              {
                  "Gmail": {"username": "me@gmail.com", "password": "abc123", "strength": "Weak"},
                  ...
              }
        Returns {} if file doesn't exist or is corrupted.
    """
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as error:
        print(f"⚠  Could not read saved data ({error}). Starting with an empty vault.")
        return {}


def save_data(data):
    """
    Save the password dictionary to the JSON file.

    Args:
        data (dict): The full password dictionary to save.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as error:
        print(f"⚠  Could not save data: {error}")


# ---------------------------------------------------------------------------
# Password Helpers — generation and strength checking
# ---------------------------------------------------------------------------


def generate_password(length=DEFAULT_LENGTH):
    """
    Generate a strong random password.

    Guarantees at least one character from each category:
    lowercase, uppercase, digit, and symbol.

    Args:
        length (int): Desired password length (enforced: MIN_LENGTH to MAX_LENGTH).

    Returns:
        str: The generated password.
    """
    length = max(MIN_LENGTH, min(length, MAX_LENGTH))

    # One character from each required category.
    required = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(SYMBOLS),
    ]

    # Fill remaining length with random characters from all categories.
    all_chars = string.ascii_letters + string.digits + SYMBOLS
    remaining = [random.choice(all_chars) for _ in range(length - len(required))]

    # Shuffle so required characters aren't always at the start.
    password_chars = required + remaining
    random.shuffle(password_chars)

    return "".join(password_chars)


def check_strength(password):
    """
    Evaluate password strength based on 5 criteria:
    1. Length >= 8
    2. Contains lowercase
    3. Contains uppercase
    4. Contains digit
    5. Contains symbol

    Args:
        password (str): The password to evaluate.

    Returns:
        str: 'Weak', 'Medium', or 'Strong'
    """
    score = sum([
        len(password) >= 8,
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in SYMBOLS for c in password),
    ])

    if score >= STRONG_THRESHOLD:
        return "Strong"
    elif score >= MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "Weak"


# ---------------------------------------------------------------------------
# Display Helpers — menu and entry formatting
# ---------------------------------------------------------------------------


def display_menu():
    """Print the main menu options."""
    print("\n" + "=" * 40)
    print("        PASSWORD MANAGER")
    print("=" * 40)
    print("1. Add a new password")
    print("2. View all passwords")
    print("3. Search password by website")
    print("4. Update a password")
    print("5. Delete a password")
    print("6. Generate a strong password")
    print("7. Exit")
    print("=" * 40)


def print_entry(website, info):
    """Print a single password entry in a formatted block."""
    print("-" * 40)
    print(f"Website : {website}")
    print(f"Username: {info.get('username', '')}")
    print(f"Password: {info.get('password', '')}")
    print(f"Strength: {info.get('strength', 'Unknown')}")


# ---------------------------------------------------------------------------
# Menu Actions — one function per menu option
# ---------------------------------------------------------------------------


def add_password(data):
    """Collect details from user and save a new password entry."""
    print("\n--- Add New Password ---")

    # Get and validate website name.
    website = input("Website/App name: ").strip()
    if not website:
        print("⚠  Website name cannot be empty. Nothing was saved.")
        return
    if find_entry(data, website):
        print(f"⚠  An entry for '{website}' already exists. Use 'Update' instead.")
        return

    # Get and validate username.
    username = input("Username/Email: ").strip()
    if not username:
        print("⚠  Username cannot be empty. Nothing was saved.")
        return

    # Get password (generated or manual).
    if get_yes_no("Generate a strong password automatically? (y/n): ") == "y":
        password = generate_password()
        print(f"Generated password: {password}")
    else:
        password = input("Enter password: ").strip()

    if not password:
        print("⚠  Password cannot be empty. Nothing was saved.")
        return

    # Save the entry.
    data[website] = {
        "username": username,
        "password": password,
        "strength": check_strength(password),
    }
    save_data(data)
    print(f"✅ Saved '{website}' (Strength: {data[website]['strength']})")


def view_passwords(data):
    """Display all saved password entries."""
    print("\n--- Saved Passwords ---")

    if not data:
        print("No passwords saved yet.")
        return

    for website, info in data.items():
        print_entry(website, info)

    print("-" * 40)
    print(f"Total entries: {len(data)}")


def search_password(data):
    """Search for an entry by website name (case-insensitive)."""
    print("\n--- Search Password ---")

    website = input("Enter website/app name to search: ").strip()
    if not website:
        print("⚠  Please enter a website name to search.")
        return

    key = find_entry(data, website)
    if key:
        print_entry(key, data[key])
    else:
        print(f"⚠  No entry found for '{website}'.")


def update_password(data):
    """Update the password for an existing entry."""
    print("\n--- Update Password ---")

    website = input("Enter website/app name to update: ").strip()
    if not website:
        print("⚠  Please enter a website name to update.")
        return

    key = find_entry(data, website)
    if not key:
        print(f"⚠  No entry found for '{website}'.")
        return

    # Get new password (generated or manual).
    if get_yes_no("Generate a new strong password automatically? (y/n): ") == "y":
        new_password = generate_password()
        print(f"Generated password: {new_password}")
    else:
        new_password = input("Enter new password: ").strip()

    if not new_password:
        print("⚠  Password cannot be empty. Update cancelled.")
        return

    # Update and save.
    data[key]["password"] = new_password
    data[key]["strength"] = check_strength(new_password)
    save_data(data)
    print(f"✅ Password for '{key}' updated successfully!")


def delete_password(data):
    """Delete an entry after user confirmation."""
    print("\n--- Delete Password ---")

    website = input("Enter website/app name to delete: ").strip()
    if not website:
        print("⚠  Please enter a website name to delete.")
        return

    key = find_entry(data, website)
    if not key:
        print(f"⚠  No entry found for '{website}'.")
        return

    if get_yes_no(f"Are you sure you want to delete '{key}'? (y/n): ") == "y":
        del data[key]
        save_data(data)
        print(f"✅ Deleted '{key}'.")
    else:
        print("Deletion cancelled.")


def generate_password_menu():
    """Generate and display a random password without saving it."""
    print("\n--- Generate Strong Password ---")

    raw_length = input(f"Enter desired password length ({MIN_LENGTH}-{MAX_LENGTH}, default {DEFAULT_LENGTH}): ").strip()

    # Parse and validate length.
    if raw_length == "":
        length = DEFAULT_LENGTH
    else:
        try:
            length = int(raw_length)
            if length < MIN_LENGTH:
                print(f"⚠  Minimum length is {MIN_LENGTH}. Using {MIN_LENGTH}.")
                length = MIN_LENGTH
            elif length > MAX_LENGTH:
                print(f"⚠  Maximum length is {MAX_LENGTH}. Using {MAX_LENGTH}.")
                length = MAX_LENGTH
        except ValueError:
            print(f"⚠  Invalid number. Using default length of {DEFAULT_LENGTH}.")
            length = DEFAULT_LENGTH

    password = generate_password(length)
    print(f"Generated password: {password}")
    print(f"Strength: {check_strength(password)}")


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------


def main():
    """Main program loop: display menu and handle user choices."""
    data = load_data()

    # Map menu choices to handler functions.
    actions = {
        "1": lambda: add_password(data),
        "2": lambda: view_passwords(data),
        "3": lambda: search_password(data),
        "4": lambda: update_password(data),
        "5": lambda: delete_password(data),
        "6": generate_password_menu,
    }

    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "7":
            print("\nGoodbye! Stay safe.")
            break

        action = actions.get(choice)
        if action is None:
            print("⚠  Invalid choice. Please select a number between 1 and 7.")
            continue

        try:
            action()
        except Exception as error:
            print(f"⚠  Something went wrong: {error}")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
