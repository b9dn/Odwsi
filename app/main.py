from flask import render_template, redirect, flash, Blueprint, request, session
from flask_login import login_required, current_user
import random
import db_operations
from forms import RegistrationForm, TransactionForm, PasswordForm, EmailForm
from app import limiter

PASSWORD_LETTERS_AUTH_LEN = 4

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
def index_login():
    if current_user.is_authenticated:
        return redirect("/profile")
    return render_template("index.html", form=EmailForm())


@main.route("/password", methods=['POST'])
@limiter.exempt
@limiter.limit("3/minute", error_message="Wyczerpano limit. Spróbuj ponownie później")
def password():
    email_form = EmailForm(request.form)

    if email_form.validate_on_submit():
        user = db_operations.get_user_by_email(email_form.email.data)

        if user is None:
            password_chars_to_check = rand_password_chars_indx(10)
            return render_template("password.html", form=PasswordForm(),
                                   pass_chars=password_chars_to_check, email=email_form.email.data)

        pass_len = db_operations.get_user_password_len(user.id)
        password_chars_to_check = rand_password_chars_indx(pass_len)
        session['pass_chars'] = password_chars_to_check

        return render_template("password.html", form=PasswordForm(),
                               pass_chars=password_chars_to_check, email=email_form.email.data)

    return redirect("/")


@main.route("/register")
def register():
    return render_template("register.html", form=RegistrationForm())


@main.route("/profile")
@login_required
def profile():
    form = TransactionForm()
    transactions_to = db_operations.get_all_to_user_transactions(current_user.id)
    transactions_from = db_operations.get_all_from_user_transactions(current_user.id)
    return render_template("profile.html", user=current_user,
                           transactions_to=transactions_to,
                           transactions_from=transactions_from,
                           form=form)


@main.route("/transaction", methods=['POST'])
@login_required
def transaction():
    form = TransactionForm(request.form)
    if form.validate_on_submit():
        if current_user.account_balance < form.amount.data:
            flash("Nie masz wystarczających środków na koncie")
            return redirect("/profile")
        destination_user = db_operations.get_user_by_account_number(form.receiverAccountNumber.data)
        if destination_user is not None:
            conn = db_operations.get_connection()
            name_and_surname_from = current_user.name + " " + current_user.surname
            conn.execute("INSERT INTO transactions "
                         "(title, amount, nameAndSurnameFrom, nameAndSurnameTo, idUserSource, idUserDestination)"
                         "VALUES (?, ?, ?, ?, ?, ?)", (form.title.data, float(form.amount.data), name_and_surname_from,
                                                       form.nameAndSurnameTo.data, current_user.id, destination_user.id))
            conn.execute("UPDATE users SET accountBalance = accountBalance - ? WHERE id = ?", (float(form.amount.data), current_user.id))
            conn.execute("UPDATE users SET accountBalance = accountBalance + ? WHERE id = ?", (float(form.amount.data), destination_user.id))
            conn.commit()
            conn.close()
            return redirect("/profile")
    flash("Nieprawidłowe dane transakcji")
    return redirect("/profile")


@main.route("/vunerable")
@login_required
def vunerable_information():
    return render_template("vunerable-information.html", user=current_user)


def rand_password_chars_indx(pass_len):
    pass_chars_to_check = []
    for _ in range(PASSWORD_LETTERS_AUTH_LEN):
        while (rand := random.randint(1, pass_len)) in pass_chars_to_check:
            pass
        pass_chars_to_check.append(rand)
    pass_chars_to_check.sort()
    return pass_chars_to_check
