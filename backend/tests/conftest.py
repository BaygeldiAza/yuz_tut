from collections.abc import AsyncGenerator
from sqlalchemy.pool import NullPool
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import(
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database.base import Base
from app.database.session import get_db
from app.models.search_history import SearchHistory
from app.models.user import User
from app.main import app


TEST_DATABASE_URL=(
    "postgresql+asyncpg://postgres:postgres@test-db:5432/yuz_tut_test"
)

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass = NullPool,
)

TestSessionLocal=async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database()-> AsyncGenerator[None, None]:

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:

    async with TestSessionLocal() as session:
        yield session 

        await session.rollback()

        await session.execute(delete(SearchHistory))
        await session.execute(delete(User))
        await session.commit()

@pytest_asyncio.fixture
async def client(db_session: AsyncSession)-> AsyncGenerator[AsyncSession,None]:

    async def override_get_db()->AsyncGenerator[AsyncGenerator, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    )as async_cliet: 
        yield async_cliet

    app.dependency_overrides.clear()