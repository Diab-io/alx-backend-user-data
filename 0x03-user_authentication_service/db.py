#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user to the database
        """
        user_obj = User(email=email, hashed_password=hashed_password)
        if not self.__session:
            self._session
        self.__session.add(user_obj)
        self.__session.commit()

        return user_obj

    def find_user_by(self, **kwargs) -> User:
        """Method used to get the user from the db
        """
        for key, value in kwargs.items():
            columns = class_mapper(User).columns
            query = self._session.query(User)
            if key not in columns:
                raise InvalidRequestError
            user = query.filter(getattr(User, key) == value).first()
            if not user:
                raise NoResultFound
            return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method that updates the user with the specified id
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self.__session.commit()
