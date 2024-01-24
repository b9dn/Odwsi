DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS passwords;
DROP TABLE IF EXISTS transactions;


CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    surname VARCHAR(255),
    pesel VARCHAR(11) UNIQUE,
    email VARCHAR(255) UNIQUE,
    documentNumber VARCHAR(9) UNIQUE,
    accountNumber VARCHAR(26) UNIQUE,
    creditCardNumber VARCHAR(16),
    accountBalance DECIMAL(10, 2)
);

CREATE TABLE passwords (
    password VARCHAR(255),
    K INTEGER,
    y_secrets VARCHAR(1024),
    idUser INTEGER REFERENCES users(id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255),
    amount DECIMAL(10, 2),
    nameAndSurnameFrom VARCHAR(255),
    nameAndSurnameTo VARCHAR(255),
    idUserSource INTEGER REFERENCES users(id),
    idUserDestination INTEGER REFERENCES users(id)
);

INSERT INTO users (name, surname, pesel, email, documentNumber, accountNumber, creditCardNumber, accountBalance)
VALUES
('Anna', 'Nowak', '89010112345', 'anna.nowak@email.pl', 'XYZ987456', '61109010140000071219812876', '1234567812345678', 3000.00),
('Piotr', 'Kowalski', '75020298765', 'piotr.kowalski@email.pl', 'ABC123789', '61109010140000071219812877', '9876543210987654', 2500.50),
('Marta', 'Wiśniewska', '88121234567', 'marta.wisniewska@email.pl', 'DEF456456', '61109010140000071219812878', '1111222233334444', 500.25),
('Tomasz', 'Kwiatkowski', '95030387654', 'tomasz.kwiatkowski@email.pl', 'GHI789456', '61109010140000071219812879', '5555666677778888', 800.75),
('Katarzyna', 'Mazurek', '80040423456', 'katarzyna.mazurek@email.pl', 'JKL012123', '61109010140000071219812880', '9999888877779999', 1200.00),
('test', 'test', '45678912563', 'test@pl.pl', 'ABC456879', '78954010140050071219812876', '4567891237984569', 9000.53);

INSERT INTO passwords (password, idUser)
VALUES
('tajneHaslo123', 1),
('bezpieczneHaslo456', 2),
('hasloMocne789', 3),
('ukryteHaslo101', 4),
('silneHaslo202', 5),
('test123', 6);

INSERT INTO transactions (title, amount, nameAndSurnameFrom, nameAndSurnameTo, idUserSource, idUserDestination)
VALUES
('Przelew za usługi', 150.00, 'Anna Nowak', 'Marta Wiśniewska', 1, 3),
('Zakupy online', 50.50, 'Piotr Kowalski', 'Tomasz Kwiatkowski', 2, 4),
('Wypłata gotówki', 200.25, 'Marta Wiśniewska', 'Katarzyna Mazurek', 3, 5),
('Przelew między kontami', 100.75, 'Tomasz Kwiatkowski', 'Anna Nowak', 4, 1),
('Opłata za usługi', 30.00, 'Katarzyna Mazurek', 'Piotr Kowalski', 5, 2);
