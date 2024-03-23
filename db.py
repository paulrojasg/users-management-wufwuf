from fastapi import HTTPException

db_users = [
    {
        "id": 0,
        "username":"leonardo_fernandez",
        "email": "leonardo@mail.com",
        "password": "12345#hash"
    },
    {
        "id": 1,
        "username":"ruben_diaz",
        "email": "ruben@mail.com",
        "password": "54321#hash"
    }
]

"""
Decodes password; converts it from hash to plain

@type password: str
@param password: Encoded password to be decoded
@rtype: str
@returns: Returns decoded password

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def decode_password(password):
    decoded_password = password.split('#')[0]

    return decoded_password


"""
Checks password

@type input_password: str
@param input_password: Password to be checked against one in database
@type stored_password: str
@param stored_password: Encoded password stored in database
@rtype: Boolean
@returns: Returns True if input_password matches stored_password, returns
          False if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def check_password(input_password, stored_password):
    decoded_password = decode_password(stored_password)

    if input_password == decoded_password:
        return True
    else:
        return False


"""
Gets user data

@type username: str
@param username: User's username to search
@type password: str
@param password: Plain password to check against the one in database
@rtype: Dict or None
@returns: Returns user's data if match was found, return None if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def get_user(username: str, password: str):
    for user in db_users:
        if user['username'] == username:
            if check_password(password, user['password']):
                user_data = user.copy()
                del user_data['password']
                return user_data
            else:
                break
    return None