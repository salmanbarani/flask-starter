import pytest
from src.domain import utils
    
VALUE_TO_HASH = "sample-value-to-hash"

def test_generate_hash_password():
    algo = utils.get_password_hash_generator()
    hashed_value = algo.generate_hash_password(VALUE_TO_HASH)
    assert len(hashed_value) > 0
    assert VALUE_TO_HASH != hashed_value

def test_check_password_hash():
    algo = utils.get_password_hash_generator()
    hashed_value = algo.generate_hash_password(VALUE_TO_HASH)
    assert algo.check_password_hash(hashed_value, VALUE_TO_HASH)