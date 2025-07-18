import pytest
from unittest.mock import AsyncMock, patch
from bson import ObjectId
from datetime import datetime, timezone

from app.models.task_model import TaskCreate
from app.models.user_model import UserInDB
from app.crud import task_crud


@pytest.mark.asyncio
async def test_create_task_returns_task():
    fake_task = TaskCreate(title="Mock title", description="Desc", status="pending")
    fake_user_id = ObjectId()
    fake_user = UserInDB(id=fake_user_id, username="u", hashed_password="p", role="user")
    fake_inserted_id = ObjectId()

    mock_insert_one = AsyncMock(return_value=AsyncMock(inserted_id=fake_inserted_id))

    with patch("app.crud.task_crud.task_collection.insert_one", mock_insert_one):
        task = await task_crud.create_task(fake_task, fake_user)

        mock_insert_one.assert_awaited_once()
        assert task.title == fake_task.title
        assert task.owner_id == str(fake_user_id)
        assert task.id == str(fake_inserted_id)


@pytest.mark.asyncio
async def test_get_task_returns_task_for_owner():
    fake_id = ObjectId()
    fake_user_id = ObjectId()
    fake_user = UserInDB(id=fake_user_id, username="u", hashed_password="p", role="user")

    mock_doc = {
        "_id": fake_id,
        "title": "Get task",
        "description": "testing get",
        "status": "pending",
        "owner_id": str(fake_user_id),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    mock_find_one = AsyncMock(return_value=mock_doc)

    with patch("app.crud.task_crud.task_collection.find_one", mock_find_one):
        task = await task_crud.get_task(str(fake_id), fake_user)

        mock_find_one.assert_awaited_once()
        assert task.id == str(fake_id)
        assert task.owner_id == str(fake_user_id)


@pytest.mark.asyncio
async def test_delete_task_returns_true_when_deleted():
    fake_id = ObjectId()
    fake_user_id = ObjectId()
    fake_user = UserInDB(id=fake_user_id, username="u", hashed_password="p", role="user")

    mock_delete_one = AsyncMock(return_value=AsyncMock(deleted_count=1))

    with patch("app.crud.task_crud.task_collection.delete_one", mock_delete_one):
        result = await task_crud.delete_task(str(fake_id), fake_user)

        mock_delete_one.assert_awaited_once()
        assert result is True
