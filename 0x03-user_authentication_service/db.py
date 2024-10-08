#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
import bcrypt


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database and returns the new user object.

        Args:
            email (str): The new user's email address.
            hashed_password (str): The new user's hashed password.

        Returns:
            User: The new user object.
        """

        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            self._session.refresh(new_user)
            return new_user
        except Exception:
            self._session.rollback()

    def find_user_by(self, **kwargs) -> User:
        """Returns the first row found in the users table that matches"""
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError
            result = (
                self._session.query(User)
                .filter(tuple_(*fields).in_([tuple(values)]))
                .first()
            )
            if result is None:
                raise NoResultFound
            return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's password"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
