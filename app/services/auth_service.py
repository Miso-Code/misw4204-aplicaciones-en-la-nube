import hashlib
from typing import Dict
from typing import Tuple

from flask_jwt_extended import create_access_token

from common.exceptions import InvalidParameterException, ResourceExistsException
from common.utils import save_changes
from common.decorators import db_session
from models.user import User


@db_session
def login(session, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    username = data.get('username')
    email = data.get('email')
    if not any([username, email]):
        raise InvalidParameterException('Username or email is required')

    user_data = username if username is not None else email
    # get the user data if the username or email matches with user
    user = session.query(User).filter(
        (User.username == user_data) | (User.email == user_data)
    ).first()

    if user:
        encrypted_password = hashlib.sha256(
            data['password'].encode('utf-8'),
        ).hexdigest()
        if user.password == encrypted_password:
            access_token = create_access_token(identity=user.id)
            response_object = {
                'status': 'success',
                'message': 'User logged in.',
                'id': user.id,
                'token': access_token,
            }
            return response_object, 200
        else:
            raise InvalidParameterException('Username/Password is incorrect')

    else:
        raise InvalidParameterException('Username/Password is incorrect')


@db_session
def signup(session, data: Dict[str, str]) -> Dict[str, str]:
    username = data.get('username')
    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not all([username, email, password1, password2]):
        raise InvalidParameterException('All fields are required.')

    if password1 != password2:
        raise InvalidParameterException('Passwords do not match.')

    user_data = username if username is not None else email
    # get the user data if the username or email matches with user
    user = session.query(User).filter(
        (User.username == user_data) | (User.email == user_data)
    ).first()

    if user:
        raise ResourceExistsException('Username/Email already exists')

    else:
        encrypted_password = hashlib.sha256(
            password1.encode('utf-8'),
        ).hexdigest()
        new_user = User(
            username=username,
            email=email,
            password=encrypted_password,
        )
        save_changes(session, new_user)
        response_object = {
            'status': 'success',
            'message': 'User created.',
            'id': new_user.id,
        }
        return response_object
