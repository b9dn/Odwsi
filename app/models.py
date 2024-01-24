from flask_login import UserMixin
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import db_operations


def decrypt(encrypted_data, key, iv):
    iv = bytes.fromhex(iv)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = bytes.fromhex(encrypted_data)
    decrypted = aes.decrypt(encrypted_data)
    return decrypted.strip(b"\x00")


class User(UserMixin):
    def __init__(self, id, name, surname, email, account_balance):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.account_balance = account_balance

    def get_pesel(self):
        conn = db_operations.get_connection()
        match = conn.execute("SELECT pesel FROM users WHERE id = ?", (self.id,)).fetchone()
        conn.close()
        if match is None:
            return None
        return match['pesel']

    def get_account_number(self):
        conn = db_operations.get_connection()
        match = conn.execute("SELECT accountNumber FROM users WHERE id = ?", (self.id,)).fetchone()
        conn.close()
        if match is None:
            return None
        return match['accountNumber']

    def get_document_number(self):
        conn = db_operations.get_connection()
        match = conn.execute("SELECT documentNumber FROM users WHERE id = ?", (self.id,)).fetchone()
        conn.close()
        if match is None:
            return None
        key = PBKDF2(b"$/Xxqq[N,Z'(yX" + bytes(self.email, "utf-8") + b"aP[d", b"l1fnC-xQ(0iO#B")
        encrypted = match['documentNumber'].split(";")
        iv = encrypted[0]
        data_encrypted = encrypted[1]
        return decrypt(data_encrypted, key, iv).decode("utf-8")

    def get_credit_card_number(self):
        conn = db_operations.get_connection()
        match = conn.execute("SELECT creditCardNumber FROM users WHERE id = ?", (self.id,)).fetchone()
        conn.close()
        if match is None:
            return None
        key = PBKDF2(b"B)C[+Dkn3*@;En" + bytes(self.email, "utf-8") + b"79gb", b"93jl*:{$8VRp[`")
        encrypted = match['creditCardNumber'].split(";")
        iv = encrypted[0]
        data_encrypted = encrypted[1]
        return decrypt(data_encrypted, key, iv).decode("utf-8")
