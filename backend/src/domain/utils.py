import abc
import werkzeug.security as hash_algorithem 


class BasePasswordHashGenerator(abc.ABC):
    """
        Base class to generate password
    """
    @abc.abstractmethod
    def generate_hash_password(self, raw_password: str) -> str:
        raise NotImplemented
    
    @abc.abstractmethod
    def check_password_hash(self, hashed_password: str, raw_password: str) -> bool:
        raise NotImplemented
    

class WerkzeugPasswordHashGenerator(BasePasswordHashGenerator):
    """
        Password Hash Generator Using Werzeug
    """
    def __init__(self) -> None:
        self.algo = hash_algorithem

    def generate_hash_password(self, raw_password: str) -> str:
        return self.algo.generate_password_hash(raw_password)

    def check_password_hash(self, hashed_password: str, raw_password: str) -> bool:
        return self.algo.check_password_hash(hashed_password, raw_password)

def get_password_hash_generator():
    return WerkzeugPasswordHashGenerator()