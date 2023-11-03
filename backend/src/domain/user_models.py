from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from . import utils, exceptions
from typing import Optional, Set, List

algo = utils.get_password_hash_generator()
class User:
    """
        User model 
    """
    def __init__(self, username, email, password,first_name, last_name, is_active,
                is_admin, created_at, updated_at) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_admin = is_admin
        self.created_at = created_at
        self.updated_at = updated_at 

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, User):
            return False
        return (__value.username == self.username) or (__value.email == self.email)

    def __hash__(self) -> int:
        return hash((self.username , self.email))
    
    def __gt__(self, __value):
        return self.created_at > __value.created_at
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def check_password(self, password: str) -> bool:
        return algo.check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username:str, email:str, password:str, *args, **kwargs) -> User:
        password = algo.generate_hash_password(password)
        now = datetime.now()
        kwargs["created_at"] = now
        kwargs["updated_at"] = now
        return cls(username, email, password, *args, **kwargs)
    
    def set_password(self, new_password: str) -> None:
        self.password = algo.generate_hash_password(new_password)

@dataclass(unsafe_hash=True)
class UserLog:
    """
        Stores all logs related to each user
    """
    user: str  # User.username
    log_type: str # UserLogTypes.
    description: str
    log_time:str # datetime


class Account:
    """
        Main entrypoint to work with User and other related Models
    """
    def __init__(self, version_number: int=0) -> None:
        self.user = None  # NOTE: it must be in set using user_set
        self._userlogs = set() # type of Set[UserLog]
        self.version_number = version_number
        self.events = [] # type of List[events.Event]

    def set_user(self, user:User) -> User:
        self.user = user.username
        self.version_number += 1
        #TODO: trigger an event
        #NOTE: log USER-CREATE 

    def add_log(self, userlog: UserLog):
        self._userlogs.add(userlog)


    def __str__(self) -> str:
        return f"Account {self.user}"
    
    def __repr__(self) -> str:
        return f"<Account {self.user}>"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value,Account):
            return False
        return (__value.user == self.user)

    def __hash__(self) -> int:
        return hash((self.user))