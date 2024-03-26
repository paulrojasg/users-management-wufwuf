from sqlalchemy import create_engine, literal
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base, User, Role, Permission, RolePermission
import os
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime

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
Hashes password given by input

@type raw_password: str
@param raw_password: Password to be hashed
@rtype: str
@returns: Hashed password

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def hash_password(raw_password):
    try:
        bytes = raw_password.encode('utf-8')
        salt = gensalt()

        hash = hashpw(bytes, salt).decode('utf-8')

        return hash

    except Exception:
        return None


"""
Check if given raw guessed password match hashed password

@type guessed_password: str
@param guessed_password: Raw password to be checked
@type hashed_password: str
@param hashed_password: Hashed password
@rtype: Boolean
@returns: True -> passwords match, False -> passwords do not match

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""


def check_password(guessed_password, hashed_password):
    try:
        guessed_bytes = guessed_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')

        return checkpw(guessed_bytes, hash_bytes)
    except Exception:
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
            'role': user.role.name,
            'role_id': user.role.id
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


"""
Creates users accounts

@type user_data: dict
@param user_data: User's data
@rtype: dict
@returns: Status which tells if creation was successfull, and if it
    isn't, tells what's wrong

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def create_user(user_data):
    try:

        new_user = User()

        # Verify if username is already used
        username = user_data['username']

        existing_user = get_user(username)

        if existing_user:
            return {'status':'username'}

        new_user.username = user_data['username']

        # Verify if email is already used

        email = user_data['email']
        query = session.query(User).filter(User.email == email)
        if session.query(literal(True)).filter(query.exists()).scalar():
            return {'status':'email'}

        new_user.email = email


        # Verify if role exists

        query = session.query(Role).filter(Role.name == user_data['role'])
        if not session.query(literal(True)).filter(query.exists()).scalar():
            return {'status': 'role'}

        role = query[0]

        new_user.role = role

        # Save rest of data
        new_user.password = user_data['password']
        new_user.age = user_data['age']
        new_user.name = user_data['name']
        new_user.lastname = user_data['lastname']

        session.add(new_user)
        session.commit()

        return {'status': 'success'}

    except Exception as e:
        print(e)
        return {'status': 'error'}


"""
Edits users accounts

@type user_data: dict
@param user_data: User's data
@rtype: dict
@returns: Status which tells if creation was successfull, and if it
    isn't, tells what's wrong

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def edit_user(user_data):
    try:

        query = session.query(User).filter(User.username == user_data['username'])

        if not session.query(literal(True)).filter(query.exists()).scalar():
            return {'status':'username'}

        user = query[0]

        # Verify if email is already used


        email = user_data['email']

        if email:
            query = session.query(User).filter(User.email == email)  
            if session.query(literal(True)).filter(query.exists()).scalar():
                return {'status':'email'}

            user.email = email


        # Verify if role exists

        query = session.query(Role).filter(Role.name == user_data['role'])
        if not session.query(literal(True)).filter(query.exists()).scalar():
            return {'status': 'role'}

        role = query[0]

        user.role = role

        # Changes password if new one is given
        if user_data['password']:
            user.password = user_data['password']
        
        user.age = user_data['age']
        user.name = user_data['name']
        user.lastname = user_data['lastname']

        user.modification_date = datetime.now().date()

        session.commit()

        return {'status': 'success'}


    except Exception as e:
        print(e)
        return {'status': 'error'}

"""
Get permission instance

@type name: str
@param name: Permission's name to search
@rtype: Dict or None
@returns: Returns permission's data if match was found, return None if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def get_permission(name):
    query = session.query(Permission).filter(Permission.name == name)

    if session.query(literal(True)).filter(query.exists()).scalar():
        permission = query[0]

        permission_data = {
            "id": permission.id,
            "name": permission.name,
            "description": permission.description,
        }

        return permission_data

    return None


"""
Get role instance

@type name: str
@param name: Role's name to search
@rtype: Dict or None
@returns: Returns role's data if match was found, return None if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def get_role(name):
    query = session.query(Role).filter(Role.name == name)

    if session.query(literal(True)).filter(query.exists()).scalar():
        role = query[0]

        role_data = {
            "id": role.id,
            "name": role.name,
            "description": role.description,
        }

        return role_data

    return None


"""
Checks if a role has some certain permissions.

@type role_name: str
@param role_name: Role to be checked
@type permissions_name: list[str]
@param permissions_name: Permissions to be checked
@rtype: Boolean
@returns: True -> role has each permission, False -> role doesn't have each permission

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def check_role_permission(role_name, permissions_names):

    role = get_role(role_name)

    if role:

        for permission_name in permissions_names:
            permission = get_permission(permission_name)

            if permission:
                query = session.query(RolePermission).filter(
                    RolePermission.role_id == role['id'], RolePermission.permission_id == permission['id']
                )

                if not session.query(literal(True)).filter(query.exists()).scalar():
                    return False

        return True

    return False


# def check_capability(role_id, permission_name):
#     query = session.query(User).filter(User.username == username)

#     if session.query(literal(True)).filter(query.exists()).scalar():

"""
Insert basic data to database

@rtype: None

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def start_database_sample():

    # Roles
    member_role = Role(name='member')
    session.add(member_role)
    admin_role = Role(name='admin')
    session.add(admin_role)

    # Permissions
    create_user_permission = Permission()
    create_user_permission.name = 'create_user'
    create_user_permission.description = 'Can create users'
    session.add(create_user_permission)

    create_member_user_permission = Permission()
    create_member_user_permission.name = 'create_member_user'
    create_member_user_permission.description = 'Can create member users'
    session.add(create_member_user_permission)

    create_admin_user_permission = Permission()
    create_admin_user_permission.name = 'create_admin_user'
    create_admin_user_permission.description = 'Can create admin users'
    session.add(create_admin_user_permission)

    edit_user_permission = Permission()
    edit_user_permission.name = 'edit_user'
    edit_user_permission.description = 'Can edit users'
    session.add(edit_user_permission)

    edit_own_user_permission = Permission()
    edit_own_user_permission.name = 'edit_own_user'
    edit_own_user_permission.description = 'Can edit own user account'
    session.add(edit_own_user_permission)

    edit_member_user_permission = Permission()
    edit_member_user_permission.name = 'edit_member_user'
    edit_member_user_permission.description = 'Can edit member users accounts'
    session.add(edit_member_user_permission)

    edit_admin_user_permission = Permission()
    edit_admin_user_permission.name = 'edit_admin_user'
    edit_admin_user_permission.description = 'Can edit admin users accounts'
    session.add(edit_admin_user_permission)

    grant_member_role_permission = Permission()
    grant_member_role_permission.name = 'grant_member_role'
    grant_member_role_permission.description = 'Can grant another user the role member'
    session.add(grant_member_role_permission)

    grant_admin_role_permission = Permission()
    grant_admin_role_permission.name = 'grant_admin_role'
    grant_admin_role_permission.description = 'Can grant another user the role admin'
    session.add(grant_admin_role_permission)


    # RolePermission
    admin_can_create_user = RolePermission()
    admin_can_create_user.permission = create_user_permission
    admin_can_create_user.role = admin_role
    session.add(admin_can_create_user)

    admin_can_create_member_user = RolePermission()
    admin_can_create_member_user.permission = create_member_user_permission
    admin_can_create_member_user.role = admin_role
    session.add(admin_can_create_member_user)

    admin_can_create_admin_user = RolePermission()
    admin_can_create_admin_user.permission = create_admin_user_permission
    admin_can_create_admin_user.role = admin_role
    session.add(admin_can_create_admin_user)

    admin_can_edit_user = RolePermission()
    admin_can_edit_user.permission = edit_user_permission
    admin_can_edit_user.role = admin_role
    session.add(admin_can_edit_user)

    member_can_edit_user = RolePermission()
    member_can_edit_user.permission = edit_user_permission
    member_can_edit_user.role = member_role
    session.add(member_can_edit_user)

    admin_can_edit_own_user = RolePermission()
    admin_can_edit_own_user.permission = edit_own_user_permission
    admin_can_edit_own_user.role = admin_role
    session.add(admin_can_edit_own_user)

    member_can_edit_own_user = RolePermission()
    member_can_edit_own_user.permission = edit_own_user_permission
    member_can_edit_own_user.role = member_role
    session.add(member_can_edit_own_user)

    admin_can_edit_member_user = RolePermission()
    admin_can_edit_member_user.permission = edit_member_user_permission
    admin_can_edit_member_user.role = admin_role
    session.add(admin_can_edit_member_user)

    admin_can_edit_admin_user = RolePermission()
    admin_can_edit_admin_user.permission = edit_admin_user_permission
    admin_can_edit_admin_user.role = admin_role
    session.add(admin_can_edit_admin_user)

    admin_can_grant_role_member = RolePermission()
    admin_can_grant_role_member.permission = grant_member_role_permission
    admin_can_grant_role_member.role = admin_role
    session.add(admin_can_grant_role_member)

    admin_can_grant_role_admin = RolePermission()
    admin_can_grant_role_admin.permission = grant_admin_role_permission
    admin_can_grant_role_admin.role = admin_role
    session.add(admin_can_grant_role_admin)

    # Users
    bob = User()
    bob.username = 'bob'
    bob.email = 'bob@mail.com'
    bob.name = 'Bob'
    bob.lastname = 'Pierce'
    bob.password = hash_password('12345')
    bob.role = member_role
    session.add(bob)

    alice = User()
    alice.username = 'alice'
    alice.email = 'alice@mail.com'
    alice.age = 24
    alice.name = 'Alice'
    alice.lastname = 'Kane'
    alice.password = hash_password('54321')
    alice.role = admin_role
    session.add(alice)

    session.commit()

def test():
    pass


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    start_database_sample()
    #test()