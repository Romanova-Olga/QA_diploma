import os
import pytest
from dotenv import find_dotenv, load_dotenv
from task_api import TaskAPI
from typing import Generator

load_dotenv(find_dotenv())


@pytest.fixture(scope="session")
def config() -> dict:
    return {
        "base_url": os.getenv ("BASE_URL"),
        "api_key": os.getenv ("API_KEY"),
        "column_id": os.getenv ("COLUMN_ID"),
        "company_id": os.getenv("COMPANY_ID"),
    }


@pytest.fixture(scope="session")
def api_client(config: dict) -> TaskAPI:
    return TaskAPI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        company_id=config["company_id"],
    )


@pytest.fixture(scope="function")
def created_task(api_client: TaskAPI,config:dict) -> Generator[str, None, None]:
    """Фикстура создает задачу перед тестом и удаляет её после (teardown)."""
   
    column_id = config["column_id"]
    response = api_client.create_task("Временная задача для теста", column_id)

    assert response.status_code == 201, f"Ошибка создания задачи: {response.text}"
    task_id = response.json()["id"]

    yield task_id

    # Teardown: удаляем задачу
    api_client.delete_task(task_id)
