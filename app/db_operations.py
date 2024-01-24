import sqlite3
from models import User

DATABASE = 'bank.db'


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_id(user_id):
    conn = get_connection()
    match = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if match is None:
        return None
    return User(match['id'], match['name'], match['surname'], match['email'], match['accountBalance'])


def get_user_by_email(user_email):
    conn = get_connection()
    match = conn.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()
    conn.close()
    if match is None:
        return None
    return User(match['id'], match['name'], match['surname'], match['email'], match['accountBalance'])


def get_user_by_account_number(user_account_number):
    conn = get_connection()
    match = conn.execute("SELECT * FROM users WHERE accountNumber = ?", (user_account_number,)).fetchone()
    conn.close()
    if match is None:
        return None
    return User(match['id'], match['name'], match['surname'], match['email'], match['accountBalance'])


def get_user_password_len(user_id):
    conn = get_connection()
    match = conn.execute("SELECT * FROM passwords WHERE idUser = ?", (user_id,)).fetchone()
    print(f"Match {match['y_secrets']}")
    conn.close()
    if match is None:
        return None
    return len(match['y_secrets'].split(","))


def does_user_with_email_exists(user_email):
    conn = get_connection()
    match = conn.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()
    conn.close()
    return False if match is None else True


def does_user_with_account_number_exists(account_number):
    conn = get_connection()
    match = conn.execute("SELECT * FROM users WHERE accountNumber = ?", (account_number,)).fetchone()
    conn.close()
    return False if match is None else True


def does_user_with_credit_card_number_exists(credit_card_number):
    conn = get_connection()
    match = conn.execute("SELECT * FROM users WHERE creditCardNumber = ?", (credit_card_number,)).fetchone()
    conn.close()
    return False if match is None else True


def get_all_to_user_transactions(user_id):
    conn = get_connection()
    match = conn.execute("SELECT * FROM transactions WHERE idUserSource = ?", (user_id,)).fetchall()
    conn.close()
    return match


def get_all_from_user_transactions(user_id):
    conn = get_connection()
    match = conn.execute("SELECT * FROM transactions WHERE idUserDestination = ?", (user_id,)).fetchall()
    conn.close()
    return match
