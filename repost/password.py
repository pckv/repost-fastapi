"""Password hashing functions."""

from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """Hash the given password using the context scheme."""
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Compare the given password with the given hashed password."""
    return password_context.verify(password, hashed_password)
