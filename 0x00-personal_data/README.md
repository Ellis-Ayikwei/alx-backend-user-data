# Personal Data - Backend Authentication

This project focuses on handling personal data securely in backend applications. It involves implementing functionalities like logging, filtering sensitive information (PII), secure database connection, and password encryption.

## Learning Objectives

By the end of this project, you should be able to:
- Identify examples of Personally Identifiable Information (PII).
- Implement a log filter to obfuscate PII fields.
- Encrypt passwords and verify their validity.
- Authenticate a database connection using environment variables.

## Requirements

- All files are written in Python 3.7 and are compatible with Ubuntu 18.04 LTS.
- Code follows `pycodestyle` style (version 2.5).
- All files must be executable and end with a new line.
- Modules, classes, and functions should have descriptive docstrings.
- All functions should be type annotated.

## Project Structure

- `filtered_logger.py`: Contains functions and classes for logging and filtering sensitive data.
- `encrypt_password.py`: Handles password hashing and validation.
- `main.py`: Example usage of functions and classes.
- `user_data.csv`: Example dataset used for filtering sensitive data.
  
## Tasks

### 0. Regex-ing
Write a function `filter_datum` that obfuscates specified fields in a log message using regular expressions.

### 1. Log Formatter
Update the `RedactingFormatter` class to filter PII fields in log records.

### 2. Create Logger
Implement a `get_logger` function that returns a `Logger` object configured with `RedactingFormatter`.

### 3. Connect to Secure Database
Implement a `get_db` function to securely connect to a MySQL database using credentials stored in environment variables.

### 4. Read and Filter Data
Implement a `main` function that retrieves and logs user data, obfuscating sensitive information.

### 5. Encrypting Passwords
Implement a `hash_password` function to securely hash passwords using bcrypt.

## Installation

To install the necessary dependencies, run:
```bash
pip3 install -r requirements.txt

