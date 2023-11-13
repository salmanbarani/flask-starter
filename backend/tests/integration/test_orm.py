from datetime import date, datetime
from src.domain.users.user_models import User, UserLog, Account
from src.domain.users.utils import UserLogTypes
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError



def get_sample_data():
   return {
            'email': "salman@gmail.com",
            'username': "salman",
            'password': "pass1234",
            'first_name': "Salman",
            'last_name': "Barani",
            'is_active': True,
            'is_admin': False,
            'created_at': "2022-01-01",
            'updated_at': "2022-01-01"
        }

def get_sample_user_log():
    return {
        'user': "salman",
        'log_type': UserLogTypes.USER_CREATED,
        'description': "user salman@gmail.com was created",
        'log_time': datetime.now()
    }

def insert_a_sample_user(session):
    session.execute(
        text(
            'INSERT INTO users (email, username, password, first_name, last_name, '
            'is_active, is_admin, created_at, updated_at) VALUES '
            '(:email, :username, :password, :first_name, :last_name, '
            ':is_active, :is_admin, :created_at, :updated_at)'
        ), get_sample_data()
    )
    session.commit()

def insert_a_sample_user_log(session):
    user_log_data = get_sample_user_log()
    insert_a_sample_user(session)
    user_log = UserLog(**user_log_data)
    session.add(user_log)
    session.commit()

def insert_a_sample_account(session):
    insert_a_sample_user(session)
    account_data = {'user': "salman", 'version_number': 1}

    session.execute(
        text(
            'INSERT INTO accounts (user, version_number) '
            'VALUES (:user, :version_number);'
        ), account_data)
    session.commit()

def test_user_mapper_can_load_data(session):
    session.execute(
        text(
            'INSERT INTO users (email, username, password, first_name, last_name, '
            'is_active, is_admin, created_at, updated_at) VALUES '
            '(:email, :username, :password, :first_name, :last_name, '
            ':is_active, :is_admin, :created_at, :updated_at)'
        ), get_sample_data()
    )

    expected = [User(** get_sample_data())]

    result = session.query(User).all()
    assert result == expected

def test_user_mapper_can_save_data(session):
    sample_input = get_sample_data()
    sample_input["created_at"] = datetime.now()
    sample_input["updated_at"] = datetime.now()
    user = User(**sample_input)
    session.add(user)
    session.commit()

    rows = list(session.execute(text('SELECT email, username, password FROM users;')))
    assert [('salman@gmail.com', 'salman', 'pass1234')] == rows

def test_creating_sample_user_with_hash_generated_password(session):
    user = User.create_user(**get_sample_data())
    session.add(user)
    session.commit()

    user_from_db = session.query(User).all()[0]
    assert get_sample_data()['password']!= user_from_db.password and len(user_from_db.password) > 0

def test_user_logs_mapper_can_load_data(session):
    insert_a_sample_user(session)
    user_log_data = get_sample_user_log()

    session.execute(
        text(
            'INSERT INTO userlogs (user, log_type, description, log_time) '
            'VALUES (:user, :log_type, :description, :log_time);'
        ), user_log_data)

    expected = [UserLog(**user_log_data)]

    result = session.query(UserLog).all()
    print(expected,"\n", result)
    assert result == expected

def test_sever_user_logs(session):
    """Test that each user can have severl logs"""
    user_log_data = get_sample_user_log()
    insert_a_sample_user(session)

    session.execute(
        text(
            'INSERT INTO userlogs (user, log_type, description, log_time) '
            'VALUES (:user, :log_type, :description, :log_time);'
        ), user_log_data)

    user_log_data['log_type'] = UserLogTypes.USER_LOGGED_IN
    user_log_data['description'] = "user just loged in"
    user_log_data['log_time'] = datetime.now()

    # adding logs for the second log
    session.execute(
        text(
            'INSERT INTO userlogs (user, log_type, description, log_time) '
            'VALUES (:user, :log_type, :description, :log_time);'
        ), user_log_data)
    session.commit()

    result = session.query(UserLog).all()

    assert len(result)  == 2
    for userlog in result:
        assert userlog.log_type in {UserLogTypes.USER_CREATED, UserLogTypes.USER_LOGGED_IN}

def test_user_log_mapper_can_save_data(session):
    user_log_data = get_sample_user_log()
    insert_a_sample_user(session)

    user_log = UserLog(**user_log_data)
    session.add(user_log)
    session.commit()

    rows = list(session.execute(text('SELECT user, log_type FROM userlogs;')))
    assert [('salman', UserLogTypes.USER_CREATED)] == rows

def test_account_mapper_can_load_data(session):
    insert_a_sample_user(session)
    account_data = {'user': "salman", 'version_number': 1}
    session.execute(
        text(
            'INSERT INTO accounts (user, version_number) '
            'VALUES (:user, :version_number);'
        ), account_data)
    result = session.query(Account).all()

    assert account_data["user"] == result[0].user

def test_two_accounts_with_the_same_user_not_possible(session):
    # Inserting the first user with id 1 
    insert_a_sample_user(session)
    account_data = {'user': "salman", 'version_number': 1}
    session.execute(
        text(
            'INSERT INTO accounts (user, version_number) '
            'VALUES (:user, :version_number);'
        ), account_data)
    session.commit()
    result = session.query(Account).all()
    assert account_data['user'] == result[0].user

    # inserting the second account with user id 1 fails
    with pytest.raises(IntegrityError): 
        session.execute(
         text(
            'INSERT INTO accounts (user, version_number) '
            'VALUES (:user, :version_number);'
         ), account_data)

def test_account_mapper_save_data(session):
    insert_a_sample_user(session)
    account_data = {'version_number': 5}
    account = Account(**account_data)
    account.set_user(User(**get_sample_data()))
    session.add(account)
    session.commit()

    rows = list(session.execute(text('SELECT id, version_number FROM accounts;')))
    assert [(1, 6)] == rows

def test_account_set_user(session):
    user = User.create_user(**get_sample_data())
    account = Account() 
    account.set_user(user)
    assert account.version_number == 1 
    session.add(account)
    session.commit()

    # getting account and user correctly
    account_from_db = session.query(Account).all()[0]
    assert account == account_from_db 
    assert account_from_db.version_number == 1
    assert account_from_db.user == user.username

def test_account_can_not_be_stored_in_db_without_user(session):
    account = Account()
    assert account.version_number == 0
    assert account.user is None
    session.add(account)
    
    with pytest.raises(IntegrityError):
        session.commit()

def test_user_log_can_be_added_to_account(session):
    account = Account() 
    account.set_user(User.create_user(**get_sample_data()))
    session.add(account)
    session.commit()

    account_from_db = session.query(Account).all()[0]
    assert len(account_from_db._userlogs) == 0 
    userlog = UserLog(**get_sample_user_log()) 
    account_from_db.add_log(userlog)
    session.add(account_from_db)
    session.commit()

    account_from_db = session.query(Account).all()[0]
    assert len(account_from_db._userlogs) == 1
    assert account_from_db._userlogs.pop() == userlog

def test_multiple_user_logs_can_be_added_to_account(session):
    account = Account()
    account.set_user(User.create_user(**get_sample_data()))
    session.add(account)
    session.commit()

    # adding multiple userlogs with differnt log time 
    account._userlogs.add(UserLog(**get_sample_user_log()))
    account._userlogs.add(UserLog(**get_sample_user_log()))
    account._userlogs.add(UserLog(**get_sample_user_log()))

    account_from_db = session.query(Account).all()[0]
    assert len(account_from_db._userlogs) == 3 
