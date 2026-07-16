# Password Manager

A simple command-line password manager built in Python. Store, manage, and generate passwords locally with ease.

## Project Structure

```
Password-manager/
├── password_manager.py   # Main application with all functionality
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── passwords.json        # Data file (auto-created, not in repo)
```

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

### Menu Options

| Option | Description |
|--------|-------------|
| 1. Add | Create a new password entry with website, username, and password |
| 2. View | Display all saved password entries |
| 3. Search | Find a specific entry by website name |
| 4. Update | Change the password for an existing entry |
| 5. Delete | Remove an entry from the vault |
| 6. Generate | Create a strong random password |
| 7. Exit | Close the program |

### Add Password (Option 1)

When you select option 1, the program will:

1. Ask for the **Website/App name** (e.g., `github.com`)
2. Ask for the **Username/Email** (e.g., `mohamed-abdina`)
3. Ask if you want to **generate a password automatically**
   - Type `y` for a strong generated password
   - Type `n` to enter your own password
4. The entry is saved and the **strength** is evaluated

**Example:**
```
--- Add New Password ---
Website/App name: github.com
Username/Email: mohamed-abdina
Generate a strong password automatically? (y/n): n
Enter password: MySecurePass123!
✅ Saved 'github.com' (Strength: Strong)
```

## Data Storage

- All passwords are stored locally in `passwords.json`
- The file is created automatically on first use
- **Note:** Passwords are stored in plain text for learning purposes. A production system would use encryption.

## Requirements

- Python 3.6 or higher
- No external packages required (uses only standard library)

## License

This project is open source and available for learning purposes.
