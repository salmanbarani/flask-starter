import abc
from typing import Set

from ..orm import user_orm
from src.domain.users import user_models

class AbstractUserRepository(abc.ABC):
    """
        Abstract Respository that all concrete repositories should extend from 
    """
    def __init__(self) -> None:
        self.seen: Set[user_models.Account] = set()

    def add(self, account: user_models.Account=None, user:user_models.User=None):
        self._add(account, user)
        self.seen.add(account)

    def get(self, username: str) -> user_models.Account:
        account = self._get(username)
        if account:
            self.seen.add(account)
        return account

    @abc.abstractmethod
    def _add(self, account: user_models.Account, user:user_models.User=None):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, username: str) -> user_models.Account:
        raise NotImplementedError


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def _add(self, account: user_models.Account, user:user_models.User=None):
        if user:
            self.session.add(user)
        if account:
            self.session.add(account)

    def _get(self, username):
        return self.session.query(user_models.Account).filter_by(user=username).first()
