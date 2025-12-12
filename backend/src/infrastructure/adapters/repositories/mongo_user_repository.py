from typing import Optional
from src.domain.entities import User
from src.application.ports.repositories import UserRepository
from src.infrastructure.database import get_database

class MongoUserRepository(UserRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    async def get_by_email(self, email: str) -> Optional[User]:
        user_doc = await self.collection.find_one({"email": email})
        if user_doc:
            return User(**user_doc)
        return None

    async def create(self, user: User) -> User:
        await self.collection.insert_one(user.model_dump())
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        user_doc = await self.collection.find_one({"id": user_id})
        if user_doc:
            return User(**user_doc)
        return None
