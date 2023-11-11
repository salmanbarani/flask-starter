from dataclasses import dataclass
from typing import Optional

class Command:
    """
        Base command 
    """

@dataclass
class CreateAccountCommand(Command):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
