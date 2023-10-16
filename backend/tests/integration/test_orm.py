from src.domain.user_models import User
import pytest
from sqlalchemy import text

def test_user_mapper_can_load_data(session):
    session.execute(
        text(
            'INSERT INTO users (email, username, password, first_name, last_name, '
            'is_active, is_admin, created_at, updated_at) VALUES '
            '(:email, :username, :password, :first_name, :last_name, '
            ':is_active, :is_admin, :created_at, :updated_at)'
        ),
        {
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
    )

    session.commit()
    result = session.query(User).all()
    # print(result)


    pytest.fail()