from src.domain.users import commands
from src.adapters.repositories  import user_repository
from src.service_layer import user_handlers
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

def test_create_account_handler(session):
    user_data =  get_user_data()
    cmd = commands.CreateAccountCommand(**user_data)
    repo = user_repository.SqlAlchemyUserRepository(session)

    user_handlers.create_account(cmd, repo)
    stored_account = repo.get(user_data['username'])

    assert stored_account.version_number == 1
    assert stored_account.user is not None 

def test_create_account_already_created_raises_error(session):
    user_data =  get_user_data()
    cmd = commands.CreateAccountCommand(**user_data)
    repo = user_repository.SqlAlchemyUserRepository(session)
    user_handlers.create_account(cmd, repo)
    
    assert repo.get(user_data['username']).version_number == 1

    with pytest.raises(user_handlers.UserAlreadyExist):
        user_handlers.create_account(cmd, repo)



# TODO: Require modificaiton, use unit-of-work for handlers
# TODO: use fakes for repository and unit of work to work with abstraction