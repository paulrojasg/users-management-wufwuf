from sqlalchemy import create_engine, literal
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base, User, Role, Permission, RolePermission
import os

load_dotenv()

db_config_context = {
    "user":os.environ.get("DATABASE_USER"),
    "name":os.environ.get("DATABASE_NAME"),
    "pass":os.environ.get("DATABASE_PASSWORD"),
    "port":os.environ.get("DATABASE_PORT"),
    "host":os.environ.get("DATABASE_HOST")
}

engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    db_config_context['user'],
    db_config_context['pass'],
    db_config_context['host'],
    db_config_context['port'],
    db_config_context['name']
))

Session = sessionmaker(bind=engine)

session = Session()


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
@type get_password: Boolean
@param include_password: True -> include password in data, False -> don't include it
    (include_password=False by default)
@rtype: Dict or None
@returns: Returns user's data if match was found, return None if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def get_user(username: str, include_password=False):
    query = session.query(User).filter(User.username == username)

    if session.query(literal(True)).filter(query.exists()).scalar():
        user = query[0]
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'age': user.age,
            'name': user.name,
            'lastname': user.lastname,
            'creation_date': user.creation_date,
            'modification_date': user.modification_date,
            'deleted_date': user.deleted_date,
            'deleted': user.deleted,
            'role': user.role.name
        }

        if not include_password:
            del user_data['password']

        return user_data

    return None


"""
Checks credentials against users data and return match

@type username: str
@param username: User's username to search
@type password: str
@param password: Plain password to check against the one in database
@rtype: Dict or None
@returns: Returns user's data if match was found, return None if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""


def check_credentials(username, password):

    user_data = get_user(username, include_password=True)

    if user_data:
        if check_password(password, user_data['password']):
            del user_data['password'] # Do not retrieve password to user!
            return user_data

    return None


def start_database_sample():

    # Roles
    member_role = Role(name='member')
    session.add(member_role)
    admin_role = Role(name='admin')
    session.add(admin_role)

    # Permissions
    view_catalog_permission = Permission(name='View catalog')
    session.add(view_catalog_permission)
    update_catalog_permission = Permission(name='Update catalog')
    session.add(update_catalog_permission)

    # RolePermission
    member_can_view_catalog = RolePermission()
    member_can_view_catalog.role = member_role
    member_can_view_catalog.permission = view_catalog_permission
    session.add(member_can_view_catalog)
    admin_can_view_catalog = RolePermission()
    admin_can_view_catalog.role = admin_role
    admin_can_view_catalog.permission = view_catalog_permission
    session.add(admin_can_view_catalog)
    admin_can_update_catalog = RolePermission()
    admin_can_update_catalog.role = admin_role
    admin_can_update_catalog.permission = update_catalog_permission
    session.add(admin_can_update_catalog)

    # Users
    bob = User()
    bob.username = 'bob'
    bob.email = 'bob@mail.com'
    bob.name = 'Bob'
    bob.lastname = 'Pierce'
    bob.password = '12345#hash'
    bob.role = member_role
    session.add(bob)

    alice = User()
    alice.username = 'alice'
    alice.email = 'alice@mail.com'
    alice.age = 24
    alice.name = 'Alice'
    alice.lastname = 'Kane'
    alice.password = '54321#hash'
    alice.role = admin_role
    session.add(alice)

    session.commit()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    start_database_sample()