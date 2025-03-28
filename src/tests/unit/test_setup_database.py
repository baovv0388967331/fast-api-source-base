from unittest.mock import AsyncMock, patch

import pytest

from src.databases.mysql import MysqlDatabase


@pytest.mark.asyncio
async def test_open_database():
    db = MysqlDatabase()
    await db.open_database()

    assert db._engine is not None
    assert db._session_maker is not None

    await db.close_database()


@pytest.mark.asyncio
async def test_close_database():
    db = MysqlDatabase()
    await db.open_database()

    mock_engine = AsyncMock()

    with patch.object(db, "get_engine", return_value=mock_engine):
        await db.close_database()
        mock_engine.dispose.assert_awaited_once()
