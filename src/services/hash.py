import bcrypt


class HashService:

    @staticmethod
    def to_hash(value: str) -> str:
        return bcrypt.hashpw(
            value.encode(encoding='utf-8'), bcrypt.gensalt()
        ).decode(encoding='utf-8')

    @staticmethod
    def check_hash(value: str, hashed_value: str) -> bool:
        return bcrypt.checkpw(
            value.encode(encoding='utf-8'),
            hashed_value.encode(encoding='utf-8')
        )
