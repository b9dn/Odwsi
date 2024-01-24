from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField, StringField, BooleanField, DecimalField
from wtforms.validators import InputRequired, Regexp, Length, EqualTo, NumberRange

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


# not used
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Regexp(email_pattern)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=20)])
    submit = SubmitField('Login')


class EmailForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Regexp(email_pattern), Length(max=40)])
    submit = SubmitField('Login')


class PasswordForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Regexp(email_pattern), Length(max=40)])
    password_ch1 = PasswordField('Password', validators=[InputRequired(), Length(max=1)])
    password_ch2 = PasswordField('Password', validators=[InputRequired(), Length(max=1)])
    password_ch3 = PasswordField('Password', validators=[InputRequired(), Length(max=1)])
    password_ch4 = PasswordField('Password', validators=[InputRequired(), Length(max=1)])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name = StringField('Imię', validators=[InputRequired(), Regexp('^[a-zA-Z]*$'), Length(min=2, max=30)])
    surname = StringField('Nazwisko', validators=[InputRequired(), Regexp('^[a-zA-Z]*$'), Length(min=2, max=30)])
    pesel = StringField('PESEL', validators=[InputRequired(), Regexp(r'^[0-9]{11}$', message='PESEL musi mieć 11 cyfr')])
    email = StringField('Email', validators=[InputRequired(), Regexp(email_pattern, message='Nieprawidłowy email'), Length(max=40)])
    documentNumber = StringField('Seria i numer dokumentu', validators=[InputRequired(), Regexp(r'^[A-Z]{3}\d{6}$', message='Niepoprawny format dokumentu')])
    password = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=20)])
    confirmPassword = PasswordField('Potwierdź hasło', validators=[InputRequired(), EqualTo('password', message='Hasła muszą być identyczne')])
    agreement = BooleanField('Zgadzam się na warunki korzystania z usług banku', validators=[InputRequired()])
    submit = SubmitField('Zarejestruj się')


class TransactionForm(FlaskForm):
    title = StringField('Tytuł', validators=[InputRequired(), Regexp('^[a-zA-Z0-9., -]*$')])
    receiverAccountNumber = StringField('Rachunek bankowy odbiorcy', validators=[InputRequired(), Regexp('^[0-9]*$')])
    nameAndSurnameTo = StringField('Imię i nazwisko odbiorcy', validators=[InputRequired(), Regexp('^[a-zA-Z]+ [a-zA-Z]*$')])
    amount = DecimalField('Kwota', validators=[InputRequired(), NumberRange(min=0, message='Wpisz poprawną kwotę')])
    submit = SubmitField('Zatwierdz i wykonaj')
