from __future__ import annotations
from datetime import date, datetime
from typing import List, Set

class User:
    """
        User model represents everything related to user
    """
    def __init__(self, username, email, password,first_name, last_name,
                created_at, updated_at) -> None:
        self.username = username
        self.email = email
        password = password
        first_name = first_name
        last_name = last_name
        is_active = is_active
        is_admin = is_admin
        created_at = created_at
        updated_at = updated_at 

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, User):
            return False
        return (__value.username == self.username) or (__value.email == self.email)

    def __hash__(self) -> int:
        return hash(self.username + self.email)
    
    def __gt__(self, __value):
        return self.created_at > __value.created_at
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    