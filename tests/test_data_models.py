from src.adapters.db.models import User

def test_user_model():
    user = User(
        email="test@example.com",
        password="hashedpassword",
        first_name="Test",
        last_name="User",
        created_at="2023-01-01T00:00:00Z"
    )
    assert user.email == "test@example.com"
    assert user.password == "hashedpassword"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert hasattr(user, 'created_at')
    assert user.created_at == "2023-01-01T00:00:00Z"
