from sqlalchemy import text
from src.domain.users import user_models
from src.service_layer import unit_of_work
import pytest


def get_user_data(username="sample-username", email="sample@email.com", password="pass1234", first_name="fname",
                  last_name="lname"): 
    return {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }

def insert_account():
    pass


def test_add_account_using_uow(session_factory):
    session = session_factory()
    user_data = get_user_data()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        user = user_models.User.create_user(**user_data)
        account = user_models.Account()
        account.set_user(user)
        uow.accounts.add(account)
        uow.commit()

    rows = session.execute(text(
        "SELECT version_number, user FROM accounts"
    )).fetchall()

    assert [(1, user_data['username'])] == rows

def test_rolls_back_uncommited_work_by_default(session_factory):
    session = session_factory()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        user = user_models.User.create_user(**get_user_data())
        account = user_models.Account()
        account.set_user(user)
        uow.accounts.add(account)

    rows = session.execute(text(
        "SELECT version_number, user FROM accounts"
    )).fetchall()

    assert rows == []

def test_rolls_back_on_error(session_factory):
    session = session_factory()
    class MyException(Exception):
        pass
    
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            with uow:
                user = user_models.User.create_user(**get_user_data())
                account = user_models.Account()
                account.set_user(user)
                uow.accounts.add(account)                
                raise MyException()
 
    rows = session.execute(text(
        "SELECT version_number, user FROM accounts"
    )).fetchall()

    assert rows == []


def test_concurrent_updates_to_version_are_not_allowed(postgres_session_factory):
    session = postgres_session_factory()

    user_data = get_user_data("one", "one@gmail.com")
    uow = unit_of_work.SqlAlchemyUnitOfWork(postgres_session_factory)
    
    with uow:
        user = user_models.User.create_user(**user_data)
        account = user_models.Account()
        account.set_user(user)
        uow.accounts.add(user=user)
        uow.commit()
        result = uow.session.execute(text("SELECT * FROM users WHERE username='one'"))
        print(result.fetchall())
        pytest.fail()
       
        # uow.commit()

    # rows = session.execute(text(
    #     "SELECT version_number, user FROM accounts"
    # )).fetchall()

    # assert [(1, user_data['username'])] == rows