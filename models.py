from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'wufwuf_user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    creation_date = Column(Date, nullable=True, default=datetime.now().date())
    modification_date = Column(Date, nullable=True, default=datetime.now().date())
    deleted_date = Column(Date, nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)
    role_id = Column(Integer, ForeignKey('wufwuf_role.id'))
    role = relationship('Role', backref='users')


class Role(Base):
    __tablename__ = 'wufwuf_role'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Permission(Base):
    __tablename__ = 'wufwuf_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class RolePermission(Base):
    __tablename__ = 'wufwuf_role_permission'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('wufwuf_role.id'))
    permission_id = Column(Integer, ForeignKey('wufwuf_permission.id'))
    role = relationship('Role', backref='role_permissions')
    permission = relationship('Permission', backref='role_permissions')


if __name__ == '__main__':
    Base.metadata.create_all()
