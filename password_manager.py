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
    2. Data helpers      -> load_data, save_data
    3. Password helpers  -> generate_password, check_strength
    4. Menu actions       -> add/view/search/update/delete/generate
    5. main()             -> ties everything together in a loop
"""

import json
import os
import random
import string


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Name of the file where all password entries are stored.
# Because this is just a filename (no folder path), it will be created
# in whatever directory you run the script from.
DATA_FILE = "passwords.json"


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def get_yes_no(prompt):
    """Get a validated y/n input from the user."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer
        print("⚠  Please enter 'y' or 'n'.")


def find_entry(data, name):
    """Find an entry by name (case-insensitive). Returns the key or None."""
    for key in data:
        if key.lower() == name.lower():
            return key
    return None


# ---------------------------------------------------------------------------
# Data helpers — reading and writing passwords.json
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
        If the file doesn't exist yet, or is empty/corrupted, returns {}
        instead of crashing the program.
    """
    # If the file has never been created, there is nothing to load.
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            content = file.read().strip()

            # An empty file is not valid JSON, so treat it as "no data".
            if not content:
                return {}

            return json.loads(content)

    except (json.JSONDecodeError, IOError) as error:
        # json.JSONDecodeError -> the file contains broken/invalid JSON
        # IOError              -> the file couldn't be opened/read (permissions, etc.)
        print(f"⚠  Could not read saved data ({error}). Starting with an empty vault.")
        return {}


def save_data(data):
    """
    Save the given dictionary to the JSON file.

    Args:
        data (dict): The full password dictionary to save.
    """
    try:
        with open(DATA_FILE, "w") as file:
            # indent=4 makes the JSON file human-readable if you open it directly.
            json.dump(data, file, indent=4)

    except IOError as error:
        print(f"⚠  Could not save data: {error}")


# ---------------------------------------------------------------------------
# Password helpers — generation and strength checking
# ---------------------------------------------------------------------------

def generate_password(length=12):
    """
    Generate a strong random password.

    The password is guaranteed to contain at least:
        - one lowercase letter
        - one uppercase letter
        - one digit
        - one symbol
    The remaining characters are filled randomly from all categories.

    Args:
        length (int): Desired password length (minimum enforced: 4).

    Returns:
        str: The generated password.
    """
    # A password shorter than 4 characters can't fit one of each required type.
    if length < 4:
        length = 4

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+"

    all_characters = lowercase + uppercase + digits + symbols

    # Step 1: guarantee one character from each category.
    required_chars = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols),
    ]

    # Step 2: fill the rest of the length with random characters from any category.
    remaining_length = length - len(required_chars)
    random_chars = [random.choice(all_characters) for _ in range(remaining_length)]

    # Step 3: combine and shuffle so the guaranteed characters aren't
    # always in the same predictable positions (e.g. always at the start).
    password_chars = required_chars + random_chars
    random.shuffle(password_chars)

    return "".join(password_chars)


def check_strength(password):
    """
    Evaluate how strong a password is.

    The check awards one point for each of these conditions:
        1. Length is at least 8 characters
        2. Contains a lowercase letter
        3. Contains an uppercase letter
        4. Contains a digit
        5. Contains a symbol

    Args:
        password (str): The password to evaluate.

    Returns:
        str: "Weak", "Medium", or "Strong"
    """
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"

    has_min_length = len(password) >= 8
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(char in symbols for char in password)

    score = sum([has_min_length, has_lower, has_upper, has_digit, has_symbol])

    if score <= 2:
        return "Weak"
    elif score in (3, 4):
        return "Medium"
    else:
        return "Strong"


# ---------------------------------------------------------------------------
# Menu display & actions
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
    """Print a single password entry in a consistent format."""
    print("-" * 40)
    print(f"Website : {website}")
    print(f"Username: {info.get('username', '')}")
    print(f"Password: {info.get('password', '')}")
    print(f"Strength: {info.get('strength', 'Unknown')}")


def add_password(data):
    """Prompt the user for details and save a new password entry."""
    print("\n--- Add New Password ---")
    website = input("Website/App name: ").strip()

    if not website:
        print("⚠  Website name cannot be empty. Nothing was saved.")
        return

    if find_entry(data, website):
        print(f"⚠  An entry for '{website}' already exists. Use 'Update' instead.")
        return

    username = input("Username/Email: ").strip()
    if not username:
        print("⚠  Username cannot be empty. Nothing was saved.")
        return

    use_generated = get_yes_no("Generate a strong password automatically? (y/n): ")
    if use_generated == "y":
        password = generate_password()
        print(f"Generated password: {password}")
    else:
        password = input("Enter password: ").strip()

    if not password:
        print("⚠  Password cannot be empty. Nothing was saved.")
        return

    strength = check_strength(password)

    # Store the new entry as a nested dictionary, keyed by website name.
    data[website] = {
        "username": username,
        "password": password,
        "strength": strength,
    }

    save_data(data)
    print(f"✅ Saved '{website}' (Strength: {strength})")


def view_passwords(data):
    """Display every saved password entry."""
    print("\n--- Saved Passwords ---")

    if not data:
        print("No passwords saved yet.")
        return

    for website, info in data.items():
        print_entry(website, info)
    print("-" * 40)
    print(f"Total entries: {len(data)}")


def search_password(data):
    """Search for a single entry by website name (case-insensitive)."""
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
    """Change the password (and strength rating) for an existing entry."""
    print("\n--- Update Password ---")
    website = input("Enter website/app name to update: ").strip()

    if not website:
        print("⚠  Please enter a website name to update.")
        return

    key = find_entry(data, website)
    if not key:
        print(f"⚠  No entry found for '{website}'.")
        return

    use_generated = get_yes_no("Generate a new strong password automatically? (y/n): ")
    if use_generated == "y":
        new_password = generate_password()
        print(f"Generated password: {new_password}")
    else:
        new_password = input("Enter new password: ").strip()

    if not new_password:
        print("⚠  Password cannot be empty. Update cancelled.")
        return

    data[key]["password"] = new_password
    data[key]["strength"] = check_strength(new_password)

    save_data(data)
    print(f"✅ Password for '{key}' updated successfully!")


def delete_password(data):
    """Remove an entry after confirming with the user."""
    print("\n--- Delete Password ---")
    website = input("Enter website/app name to delete: ").strip()

    if not website:
        print("⚠  Please enter a website name to delete.")
        return

    key = find_entry(data, website)
    if not key:
        print(f"⚠  No entry found for '{website}'.")
        return

    confirm = get_yes_no(f"Are you sure you want to delete '{key}'? (y/n): ")
    if confirm == "y":
        del data[key]
        save_data(data)
        print(f"✅ Deleted '{key}'.")
    else:
        print("Deletion cancelled.")


def generate_password_menu():
    """Let the user generate a password without saving it to an entry."""
    print("\n--- Generate Strong Password ---")
    raw_length = input("Enter desired password length (min 4, default 12): ").strip()

    if raw_length == "":
        length = 12
    else:
        try:
            length = int(raw_length)
            if length < 4:
                print("⚠  Minimum length is 4. Using 4.")
                length = 4
            elif length > 64:
                print("⚠  Maximum length is 64. Using 64.")
                length = 64
        except ValueError:
            print("⚠  Invalid number entered. Using default length of 12.")
            length = 12

    password = generate_password(length)
    strength = check_strength(password)
    print(f"Generated password: {password}")
    print(f"Strength: {strength}")


# ---------------------------------------------------------------------------
# Main program loop
# ---------------------------------------------------------------------------

def main():
    """Load data, then loop showing the menu until the user exits."""
    data = load_data()

    # Map each menu number to the function that should handle it.
    # This avoids a long chain of if/elif statements.
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

        # Wrap each action so one unexpected error doesn't crash the whole program.
        try:
            action()
        except Exception as error:
            print(f"⚠  Something went wrong: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Lets the user press Ctrl+C to quit without an ugly traceback.
        print("\n\nInterrupted. Goodbye!")
