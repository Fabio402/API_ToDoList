import hashlib
from fastapi import FastAPI
from Model import connection, User, Token
import re
from secrets import token_hex


class Encryption:

    @classmethod
    def create_hash(cls, password: str):
        """
        :param password: that contains the sentence to be encrypted;
        :type password: ``str``

        :return: the hexadecimal value of the param.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def check_password(cls, password: str, encrypted_pass: str):
        """
        Verifies if the password inserted is the same of the user.
        :param password: string recived from user;
        :type password: ``str``
        :param encrypted_pass:  string on database;
        :type encrypted_pass: ``str``

        :return: bool informing true if matches.
        """
        if hashlib.sha256(password.encode()).hexdigest() == encrypted_pass:
            return True
        else:
            return False


def validate(name, email, password):
    """
    Validates if the user's information agrees with the terms to save.
    :param name: must have from 3 to 50 letters;
    :type name: ``str``
    :param email: must have less than 100 letters;
    :type email: ``str``
    :param password:
    :type password: ``str``

    :return: string of error or 0 for sucess.
    """
    if len(name) >= 50 or len(name) < 2:
        return 'Nome deve conter entre 3 e 50 caracteres'
    elif len(email) > 100:
        return 'E-mail deve conter menos de 100 caracteres'
    elif len(password) < 6 or len(password) > 20:
        if len(password or ()) < 6:
            return 'A senha deve conter no mínimo 6 caracteres'
        if len(re.findall(r"[A-Z]", password)) < 1:
            return 'Senha deve conter no mínimo uma letra maiusculas'
        if len(re.findall(r"[a-z]", password)) < 1:
            return 'Senha deve conter no mínimo uma letra minúscula'
        if len(re.findall(r"[0-9]", password)) < 1:
            return 'Senha deve conter no mínimo um número'
        if len(re.findall(r"[~`!@#$%^&*()_+=-{};:'><]", password)) < 1:
            return 'Senha deve conter no mínimo uma caractere especial'
    else:
        return 0


def exists(email):
    """
    Verifies if the email is been used by a User;
    :param email: str, value to check
    :type email: ``str``

    :return: bool, exists or doesn't exist.
    """
    if len(User.search(email=email)) == 0:
        return 0
    else:
        return 1


def search(**kargs):
    """
    Search method to find Users with the kargs.
    :param kargs:
        types of search
    :keyword id: searches a user using the id value
    :keyword name: searches users using the name value;
    :keyword email: searches a user using the email value;

    :return: a list with objects of User type.
    """
    session = connection()
    users = session.query(User).all()
    for key, value in kargs.items():
        if key == 'id':
            users = list(filter(lambda user: user.id == value, users))
        if key == 'nome':
            users = list(filter(lambda user: user.name == value, users))
        if key == 'email':
            users = list(filter(lambda user: user.email == value, users))
    return users


app = FastAPI()


@app.post('/login')
def login(email: str, password: str):
    """
    Verifies the user and if matches dives him an access token, returns a status dictionary
    :param email: str, user identification param;
    :param password: str, login validation param;

    :return: validation_token: str with the generated token.
    """
    session = connection()
    aux = session.query(User).filter_by(email=email).all()
    if len(aux) == 1:
        if Encryption.check_password(password, aux[0].password):
            while True:
                token = token_hex(50)
                token_exists = session.query(Token).filter_by(token=token).all()
                if len(token_exists) == 0:
                    user_exists = session.query(Token).filter_by(user_id=aux[0].id).all()
                    if len(user_exists) == 0:
                        new_token = Token(user_id=aux[0].id, token=token)
                        session.add(new_token)
                    elif len(user_exists) == 1:
                        user_exists[0].token = token
                    session.commit()
                    break
            return token
        else:
            return {'status': 'Erro!\nSenha incorreta'}
    else:
        return {'status': 'Erro!\nE-mail não cadastrado'}


@app.post('/cadastrar')
def add(name: str, email: str, password: str):
    """
    Adds a user on database and returns a dictionary with the status

    :param name: user's name
    :type name: ``str``
    :param email: user identification param
    :type email: ``str``
    :param password: user validation param
    :type email: ``str``

    :return: status (succeso or erro)
    """
    aux = exists(email)
    if not aux:
        aux = validate(name, email, password)
        if isinstance(aux, int):
            session = connection()
            hashed = Encryption.create_hash(password)
            user = User(name=name, email=email, password=hashed)
            session.add(user)
            session.commit()
            return{'status': 'sucesso'}
        else:
            return {'status': 'Erro!\n' + aux}
    else:
        return {'status': 'Erro!\nUsuário já está cadastrado'}
