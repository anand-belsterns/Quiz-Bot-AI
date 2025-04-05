import pytest

@pytest.fixture
def user_details():
    from userdetails import UserDetails
    return UserDetails(name='John Doe', age=30)