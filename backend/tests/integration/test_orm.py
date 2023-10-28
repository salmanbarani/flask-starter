from datetime import date, datetime
from src.domain.user_models import User, UserLog, Account
from src.domain.utils import UserLogTypes
import pytest
from sqlalchemy import text

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
    user_id= session.execute(text('SELECT id FROM users;')).fetchone()[0]
    user_log_data["user_id"] = user_id

    user_log = UserLog(**user_log_data)
    session.add(user_log)
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

# def test_user_logs_mapper_can_load_data(session):
#     user_log_data = get_sample_user_log()
#     insert_a_sample_user(session)
#     user_id= session.execute(text('SELECT id FROM users;')).fetchone()[0]
#     user_log_data["user_id"] = user_id

#     session.execute(
#         text(
#             'INSERT INTO userlogs (user_id, log_type, description, log_time) '
#             'VALUES (:user_id, :log_type, :description, :log_time);'
#         ), user_log_data)

#     expected = [UserLog(**user_log_data)]

#     result = session.query(UserLog).all()
#     print(expected,"\n", result)
#     assert result == expected


# def test_sever_user_logs(session):
#     """Test that each user can have severl logs"""
#     user_log_data = get_sample_user_log()
#     insert_a_sample_user(session)
#     user_id= session.execute(text('SELECT id FROM users;')).fetchone()[0]
#     user_log_data["user_id"] = user_id

#     session.execute(
#         text(
#             'INSERT INTO userlogs (user_id, log_type, description, log_time) '
#             'VALUES (:user_id, :log_type, :description, :log_time);'
#         ), user_log_data)

#     user_log_data['log_type'] = UserLogTypes.USER_LOGGED_IN
#     user_log_data['description'] = "user just loged in"
#     user_log_data['log_time'] = datetime.now()

#     # adding logs for the second log
#     session.execute(
#         text(
#             'INSERT INTO userlogs (user_id, log_type, description, log_time) '
#             'VALUES (:user_id, :log_type, :description, :log_time);'
#         ), user_log_data)
#     session.commit()

#     result = session.query(UserLog).all()
    
#     for userlog in result:
#         assert userlog.log_type in {UserLogTypes.USER_CREATED, UserLogTypes.USER_LOGGED_IN}


# def test_user_log_mapper_can_save_data(session):
#     user_log_data = get_sample_user_log()
#     insert_a_sample_user(session)
#     user_id= session.execute(text('SELECT id FROM users;')).fetchone()[0]
#     user_log_data["user_id"] = user_id

#     user_log = UserLog(**user_log_data)
#     session.add(user_log)
#     session.commit()

#     rows = list(session.execute(text('SELECT user_id, log_type FROM userlogs;')))
#     assert [(user_id, UserLogTypes.USER_CREATED)] == rows

# def test_account_mapper_can_save_data(session):
#     insert_a_sample_user_log(session)
#     account_data = {'user_id': 1, 'version_number': 1}
#     session.execute(
#         text(
#             'INSERT INTO accounts (user_id, version_number) '
#             'VALUES (:user_id, :version_number);'
#         ), account_data)

#     expected = [Account(**account_data)]

#     result = session.query(Account).all()



#     pytest.fail()



    