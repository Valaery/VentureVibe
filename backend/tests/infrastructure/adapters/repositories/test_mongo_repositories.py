import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.infrastructure.adapters.repositories.mongo_user_repository import MongoUserRepository
from src.infrastructure.adapters.repositories.mongo_repositories import MongoProductIdeaRepository, MongoResearchResultRepository
from src.domain.entities import User, ProductIdea, ResearchResult
from src.domain.value_objects import Email, HashedPassword, Content, FeasibilityScore

class TestMongoUserRepository:
    @pytest.fixture
    def mock_db(self):
        return Mock()

    @pytest.fixture
    def mock_collection(self, mock_db):
        collection = Mock()
        mock_db.users = collection
        return collection

    @patch('src.infrastructure.adapters.repositories.mongo_user_repository.get_database')
    def test_init(self, mock_get_db, mock_db):
        mock_get_db.return_value = mock_db
        repo = MongoUserRepository()
        assert repo.collection == mock_db.users

    @patch('src.infrastructure.adapters.repositories.mongo_user_repository.get_database')
    async def test_create(self, mock_get_db, mock_collection):
        mock_get_db.return_value = Mock(users=mock_collection)
        mock_collection.insert_one = AsyncMock()
        
        repo = MongoUserRepository()
        user = User(email=Email(root="test@test.com"), hashed_password=HashedPassword(root="pass"))
        
        saved_user = await repo.create(user)
        
        assert saved_user == user
        mock_collection.insert_one.assert_called_once()

    @patch('src.infrastructure.adapters.repositories.mongo_user_repository.get_database')
    async def test_get_by_email_found(self, mock_get_db, mock_collection):
        mock_get_db.return_value = Mock(users=mock_collection)
        user_data = User(email=Email(root="test@test.com"), hashed_password=HashedPassword(root="pass")).model_dump()
        mock_collection.find_one = AsyncMock(return_value=user_data)
        
        repo = MongoUserRepository()
        user = await repo.get_by_email("test@test.com")
        
        assert user is not None
        assert user.email.root == "test@test.com"
        mock_collection.find_one.assert_called_once_with({"email": "test@test.com"})

    @patch('src.infrastructure.adapters.repositories.mongo_user_repository.get_database')
    async def test_get_by_email_not_found(self, mock_get_db, mock_collection):
        mock_get_db.return_value = Mock(users=mock_collection)
        mock_collection.find_one = AsyncMock(return_value=None)
        
        repo = MongoUserRepository()
        user = await repo.get_by_email("missing@test.com")
        
        assert user is None

class TestMongoProductIdeaRepository:
    @pytest.fixture
    def mock_collection(self):
        return Mock()

    @patch('src.infrastructure.adapters.repositories.mongo_repositories.get_database')
    async def test_create(self, mock_get_db, mock_collection):
        mock_get_db.return_value = Mock(product_ideas=mock_collection)
        mock_collection.insert_one = AsyncMock()
        
        repo = MongoProductIdeaRepository()
        idea = ProductIdea(user_id="u1", content=Content(root="Valid Idea Content"))
        
        await repo.create(idea)
        
        mock_collection.insert_one.assert_called_once()

    @patch('src.infrastructure.adapters.repositories.mongo_repositories.get_database')
    async def test_get_by_user_id(self, mock_get_db, mock_collection):
        mock_get_db.return_value = Mock(product_ideas=mock_collection)
        
        # Mocking async iterator for find calls
        idea1 = ProductIdea(user_id="u1", content=Content(root="Idea 1 Content")).model_dump()
        idea2 = ProductIdea(user_id="u1", content=Content(root="Idea 2 Content")).model_dump()
        
        async def async_iter():
            for doc in [idea1, idea2]:
                yield doc
                
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.side_effect = async_iter
        mock_collection.find.return_value = mock_cursor

        repo = MongoProductIdeaRepository()
        results = await repo.get_by_user_id("u1")
        
        assert len(results) == 2
        assert results[0].user_id == "u1"
