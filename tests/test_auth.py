import pytest
from modules import auth, validators

def test_valid_email():
    assert validators.is_valid_email("test@example.com")
    assert not validators.is_valid_email("invalid-email")

def test_valid_mobile():
    assert validators.is_valid_mobile("9876543210")
    assert not validators.is_valid_mobile("12345")

def test_password_strength():
    assert validators.is_valid_password("secure123")
    assert not validators.is_valid_password("123")

def test_user_registration_and_login():
    user_id = "test_user"
    name = "Test User"
    mobile = "9876543210"
    email = "testuser@example.com"
    password = "secure123"
    role = "Student"

    # Register user
    result = auth.register_user(user_id, name, mobile, email, password, role)
    assert result is True

    # Login user
    login_result = auth.login_user(email, password)
    assert login_result is not None
    assert login_result[0] == user_id
