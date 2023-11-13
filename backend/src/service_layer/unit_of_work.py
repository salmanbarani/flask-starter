from __future__ import annotations
import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm.session import Session

from src import config
from src.adapters.repositories import user_repository


class AbstractAccountUnitOfWork(abc.ABC):
    accounts: user_repository.AbstractUserRepository

    def __enter__(self) -> AbstractAccountUnitOfWork:
        return self
    
    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()


    def collect_new_event(self):
       for account in self.accounts.seen:
           while account.events:
               yield account.events.pop(0) 
             
    @abc.abstractmethod 
    def _commit(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(
#         config.get_postgres_uri(),
#         isolation_level="REPEATABLE READ",
#     )
# )

class SqlAlchemyUnitOfWork(AbstractAccountUnitOfWork):
    def __init__(self, session_factory ) -> None: # TODO: uncomment =DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> AbstractAccountUnitOfWork:
        self.session = self.session_factory() # type : session
        self.accounts = user_repository.SqlAlchemyUserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
       self.session.commit() 

    def rollback(self):
        self.session.rollback()