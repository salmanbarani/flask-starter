from datetime import date, datetime
from src.domain.user_models import User
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

def test_user_mapper_can_save_lines(session):
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