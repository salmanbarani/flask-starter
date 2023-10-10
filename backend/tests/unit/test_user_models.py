import pytest
from datetime import datetime
from src.domain.user_models import User

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


def test_user():
    sample_user_data = get_user_data()
    user = User(**sample_user_data)
    assert user.full_name == "{} {}".format(sample_user_data["first_name"], sample_user_data["last_name"])
    for key in sample_user_data.keys():
        assert getattr(user, key) == sample_user_data[key]

def test_user_equality():
    """Users with the same username or email are equal"""
    sample_user_data = get_user_data()
    user1 = User(**sample_user_data)
    user2 = User(**sample_user_data)
    assert user1 == user2

    user2.username = "different-username"
    assert user1 == user2 # email is still equal

    user2.username = user1.username
    user2.email = "differnt@email.com"
    assert user1 == user2 # username is still equal
    
    user2.username = "different-username"
    assert user1 != user2 # both email and username are different

def test_create_user():
    sample_user_data = get_user_data()
    sample_user_data.pop("created_at")
    sample_user_data.pop("updated_at")
    user = User.create_user(**sample_user_data)
    
    password = sample_user_data.pop("password")
    assert user.password != password
    for key in sample_user_data.keys():
        assert getattr(user, key) == sample_user_data[key]
    assert user.check_password(password)

def test_set_password():
    sample_user_data = get_user_data()
    user = User(**sample_user_data)
    password = sample_user_data.pop("password")
    assert password == user.password
    user.set_password(password)
    assert password != user.password
