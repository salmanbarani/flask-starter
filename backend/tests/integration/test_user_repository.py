import pytest
from datetime import datetime

from src.adapters.repositories import user_repository
from src.domain.users import user_models


def get_user_data(username="sample-username", email="sample@email.com", password="pass1234", first_name="fname",
                  last_name="lname", is_active=True, is_admin=False, created_at=datetime.now(), updated_at=datetime.now()):
    return {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "is_active": is_active,
        "is_admin": is_admin,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def test_user_repository(session_factory):
    session = session_factory()
    repo = user_repository.SqlAlchemyUserRepository(session)

    account1 = user_models.Account()
    account2 = user_models.Account()
    account1.set_user(user_models.User(**get_user_data("first-user", "first@user.com"))) 
    account2.set_user(user_models.User(**get_user_data("second-user", "second@user.com"))) 

    repo.add(account1)
    repo.add(account2)
    repo.session.commit()

    assert repo.get(account1.user) == account1
    assert repo.get(account2.user) == account2