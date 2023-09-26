import abc
import werkzeug.security as hash_algorithem 


class BasePasswordHashGenerator(abc.ABC):
    """
        Base class to generate password
    """
    @abc.abstractmethod
    def generate_hash_password(self, raw_password):
        raise NotImplemented
    
    @abc.abstractmethod
    def check_password_hash(self, hashed_password, raw_password):
        raise NotImplemented
    

class WerkzeugPasswordHashGenerator(BasePasswordHashGenerator):
    """
        Password Hash Generator Using Werzeug
    """
    def __init__(self) -> None:
        self.algo = hash_algorithem

    def generate_hash_password(self, raw_password):
        self.algo.generate_password_hash(raw_password)

    def check_password_hash(self, hashed_password, raw_password):
        self.algo.check_password_hash(hashed_password, raw_password)