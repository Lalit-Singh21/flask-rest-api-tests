# from werkzeug.security import safe_str_cmp
from werkzeug.security import hmac
from models.user import UserModel

def authenticate(username, password):
    """
    function that gets called when a user calls the /auth endpoint
    with their username and password
    :param username: user's username is in string format
    :param password: user's un-encrypted password in string format
    :return: A user if authentication was successful, None otherwise
    """
    user = UserModel.find_by_username(username)
    # if user and safe_str_cmp(user.password, password):
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT
    verified the their authentication header is correct.
    :param payload: A dictionary with 'identity' key, which is the user id.
    :return: A userModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)