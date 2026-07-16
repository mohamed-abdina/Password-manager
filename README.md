# Password Manager

A simple command-line password manager built in Python. Store, manage, and generate passwords locally with ease.

## Features

- **Add** new password entries with website, username, and password
- **View** all saved passwords in a clean format
- **Search** for entries by website name (case-insensitive)
- **Update** existing passwords
- **Delete** entries with confirmation
- **Generate** strong random passwords with customizable length
- **Password strength** evaluation (Weak/Medium/Strong)

## How to Run

```bash
python password_manager.py
```

## Usage

When you run the program, you'll see a menu with 7 options:

```
========================================
        PASSWORD MANAGER
========================================
1. Add a new password
2. View all passwords
3. Search password by website
4. Update a password
5. Delete a password
6. Generate a strong password
7. Exit
========================================
```

Simply enter the number of the action you want to perform.

## Data Storage

- All passwords are stored locally in `passwords.json`
- The file is created automatically on first use
- **Note:** Passwords are stored in plain text for learning purposes. A production system would use encryption.

## Requirements

- Python 3.6 or higher
- No external packages required (uses only standard library)

## License

This project is open source and available for learning purposes.
