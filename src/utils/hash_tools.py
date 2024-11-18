import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(encoding='utf-8'), bcrypt.gensalt()
    ).decode(encoding='utf-8')


def check_password(stored_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        stored_password.encode(encoding='utf-8'),
        hashed_password.encode(encoding='utf-8')
    )
