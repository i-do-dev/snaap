from src.core.entities.user import User, SecureUser
from api.contracts.requests.user import UserSignUpRequest
from api.contracts.responses.user import UserProfileResponse, UserSignUpResponse
from src.core.services.password_hasher import IPasswordHasher
from src.core.value_objects.password import PlainPassword

class UserMapper:
    """User mapper to convert between Model, Entity, and Response"""
     
    @staticmethod
    def signup_request_to_entity(request: UserSignUpRequest, password_hasher: IPasswordHasher) -> SecureUser:
        fields_mapping = {
            'username': request.username,
            'email': request.email,
            'first_name': request.first_name,
            'last_name': request.last_name
        }
        
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        """Create domain entity from signup request."""
        secure_user = SecureUser(**kwargs)
        secure_user.set_password(PlainPassword(request.password), password_hasher)
        return secure_user
    
    @staticmethod
    def entity_to_signup_response(entity: User) -> UserSignUpResponse:
        """Convert domain entity to UserSignUpResponse."""
        fields_mapping = {
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'joined_at': entity.created_at.strftime("%m/%d/%Y %I:%M:%S %p") if entity.created_at else None
        }
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserSignUpResponse(**kwargs)
    
    @staticmethod
    def entity_to_profile_response(entity: User) -> UserProfileResponse:
        """Convert domain entity to UserProfileResponse."""
        fields_mapping = {
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'joined_at': entity.created_at.strftime("%m/%d/%Y %I:%M:%S %p") if entity.created_at else None
        }
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserProfileResponse(**kwargs)
    
