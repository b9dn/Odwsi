import sqlite3
from flask import render_template, Blueprint, redirect, flash, request, session
from flask_login import login_required, logout_user, login_user
import random, time
import numpy as np
from Crypto.Cipher import AES
import bcrypt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from forms import RegistrationForm, PasswordForm
from models import User
from app import limiter
import db_operations

auth = Blueprint("auth", __name__)

PASSWORD_LETTERS_AUTH_LEN = 4

def nullpadding(data, length=16):
    return data + b"\x00" * (length - len(data) % length)


def encrypt(data, key, iv):
    data = nullpadding(bytes(data, "utf-8"))
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(data)
    return encrypted


def encrypt_account_and_card_number(document_number, credit_card_number, email):
    key_document = PBKDF2(b"$/Xxqq[N,Z'(yX" + bytes(email, "utf-8") + b"aP[d", b"l1fnC-xQ(0iO#B")
    key_card = PBKDF2(b"B)C[+Dkn3*@;En" + bytes(email, "utf-8") + b"79gb", b"93jl*:{$8VRp[`")

    iv_document = get_random_bytes(16)
    iv_card = get_random_bytes(16)

    enc_document = iv_document.hex() + ";" + encrypt(document_number, key_document, iv_document).hex()
    enc_card = iv_card.hex() + ";" + encrypt(credit_card_number, key_card, iv_card).hex()

    return enc_document, enc_card


def clear_session_data():
    if 'pass_chars' in session:
        session.pop('pass_chars')


@auth.route("/auth/login", methods=['POST'])
@limiter.limit("3/minute", error_message="Wyczerpano limit. Spróbuj ponownie później")
def login():
    time.sleep(2)
    form = PasswordForm(request.form)

    if form.validate_on_submit():
        conn = db_operations.get_connection()
        match = conn.execute("SELECT * FROM users WHERE email = ?", (form.email.data,)).fetchone()
        if match is None:
            conn.close()
            clear_session_data()
            flash("Incorrect email or password")
            return redirect("/")

        password_dict = conn.execute("SELECT * FROM passwords WHERE idUser = ?", (match['id'],)).fetchone()

        if 'pass_chars' in session:
            password_chars_to_check = session['pass_chars']
        else:
            conn.close()
            clear_session_data()
            return redirect("/")

        provided_pass = [form.password_ch1.data, form.password_ch2.data,
                         form.password_ch3.data, form.password_ch4.data]

        if check_password(provided_pass, password_dict, password_chars_to_check):
            login_user(User(match['id'], match['name'], match['surname'], match['email'], match['accountBalance']))
            conn.close()
            clear_session_data()
            return redirect("/profile")

    clear_session_data()
    flash("Incorrect email or password")
    return redirect("/index")


@auth.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return redirect("/index")


@auth.route("/auth/register", methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if db_operations.does_user_with_email_exists(form.email.data):
            flash("Email address already exists")
            return redirect("/register")

        conn = db_operations.get_connection()
        while db_operations.does_user_with_account_number_exists(
                account_number := ''.join(str(random.randint(0, 9)) for _ in range(26))
        ):
            pass
        while db_operations.does_user_with_credit_card_number_exists(
                credit_card_number := ''.join(str(random.randint(0, 9)) for _ in range(16))
        ):
            pass

        (document_number, credit_card_number) = encrypt_account_and_card_number(
            form.documentNumber.data, credit_card_number, form.email.data)

        try:
            conn.execute("INSERT INTO users "
                         "(name, surname, pesel, email, documentNumber, accountNumber, creditCardNumber, accountBalance) "
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (form.name.data, form.surname.data, form.pesel.data, form.email.data, document_number,
                          account_number, credit_card_number, 0))
            conn.commit()
            user_id = db_operations.get_user_by_email(form.email.data).id

            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(bytes(form.password.data, "utf-8"), salt)
            K = int.from_bytes(password[-4:], byteorder='big')
            y_secrets = generate_y_secrets(K, form.password.data)
            y_secrets_str = ",".join(map(str, y_secrets))

            conn.execute("INSERT INTO passwords (password, K, y_secrets, idUser) VALUES (?, ?, ?, ?)",
                         (password, K, y_secrets_str, user_id))

            conn.commit()
        except sqlite3.Error as e:
            flash(e)
            return redirect("/register")
        except Exception as e:
            print(e)
            flash("Error occurred, try again later")
            return redirect("/register")
        finally:
            if conn:
                conn.close()
                return render_template("register-state.html")
    for err in form.errors.values():
        flash(err)
    return redirect("/register")


def generate_y_secrets(K, password):
    ret = []
    coefficients = np.array([random.randint(-500, 500) for _ in range(PASSWORD_LETTERS_AUTH_LEN - 1)])
    coefficients = np.hstack((coefficients, K))
    x_values = [x for x in range(1, len(password) + 1)]
    for (xi, p) in zip(x_values, password):
        yi = np.polyval(coefficients, xi)
        ret.append(yi - ord(p))
    return ret


def check_password(password_potential, password_dict, password_chars_to_check):
    K = password_dict['K']

    y_secrets = password_dict['y_secrets']
    y_secrets = [int(y) for y in y_secrets.split(",")]

    # yi = []
    # for i in password_chars_to_check:
    #     yi.append(y_secrets[i] + ord(password_potential[i]))

    ########
    K0 = 0
    for (i, c) in zip(password_chars_to_check, password_potential):
        PI_j = 1
        PI_j_minus_i = 1
        for j in password_chars_to_check:
            if j == i:
                continue
            PI_j *= j
            PI_j_minus_i *= j - i

        K0 += (y_secrets[i-1] + ord(c)) * PI_j / PI_j_minus_i
    return K0 == K

    # yi = np.array(yi, dtype=int)
    # yi = yi.reshape(len(yi), 1)

    # X*C = Y
    # szukane - C
    # X = np.zeros((PASSWORD_LETTERS_AUTH_LEN, PASSWORD_LETTERS_AUTH_LEN))
    # for i in range(PASSWORD_LETTERS_AUTH_LEN):
    #     x_column = np.array(x_values)
    #     x_column = x_column ** (PASSWORD_LETTERS_AUTH_LEN - i - 1)
    #     X[:,i] = x_column

    # C = np.linalg.solve(X, yi)
    # return equals_approx(C[len(C)-1], K)
