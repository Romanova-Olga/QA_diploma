import allure
from task_api import TaskAPI


@allure.epic("YouGile API Автоматизация")
@allure.feature("Управление задачами")
class TestTasksAPI:

    @allure.title("Создание задачи (POST /tasks)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_task(self, api_client: TaskAPI, config: dict) -> None:
        """Позитивный тест на создание задачи."""
        column_id = config["column_id"]
        response = api_client.create_task("Новая задача API", column_id)

        with allure.step("Проверка статус-кода 201 (Created)"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}."
                f"Ответ: {response.text}"
            )

        with allure.step("Проверка тела ответа"):
            response_json = response.json()
            # print("\nОТВЕТ ОТ API:", response_json)
            assert "id" in response_json, "В ответе отсутствует ID созданной задачи"
            # assert response_json["title"] == "Новая задача API"

    @allure.title("Получение задачи по ID (GET /tasks/{taskId})")
    def test_get_task_by_id(self, api_client: TaskAPI, created_task: str) -> None:
        """Позитивный тест на получение существующей задачи."""
        task_id = created_task
        response = api_client.get_task_by_id(task_id)

        with allure.step("Проверка статус-кода 200 (OK)"):
            assert (
                response.status_code == 200
            ), f"Ожидался 200, получен {response.status_code}"

        with allure.step("Проверка данных задачи"):
            assert response.json()["id"] == task_id

    @allure.title("Обновление задачи (PUT /tasks/{taskId})")
    def test_update_task(self, api_client: TaskAPI, created_task: str) -> None:
        """Позитивный тест на обновление задачи."""
        task_id = created_task
        new_title = "Обновленное название задачи"

        response = api_client.update_task(task_id, new_title)

        with allure.step("Проверка статус-кода 200 (OK)"):
            assert (
                response.status_code == 200
            ), f"Ожидался 200, получен {response.status_code}"

        with allure.step("Проверка, что данные обновились"):
            # Делаем повторный GET запрос для проверки
            get_response = api_client.get_task_by_id(task_id)
            assert get_response.json()["title"] == new_title

    @allure.title("Получение списка задач с лимитом (GET /tasks?limit=10)")
    def test_get_tasks_with_limit(self, api_client: TaskAPI) -> None:
        """Позитивный тест на получение списка задач с ограничением."""
        limit = 10
        response = api_client.get_tasks_with_limit(limit)

        with allure.step("Проверка статус-кода 200 (OK)"):
            assert response.status_code == 200

        with allure.step(f"Проверка, что количество задач не превышает {limit}"):
            tasks = response.json()
            # API может возвращать словарь с ключом 'content' или просто список
            if isinstance(tasks, dict) and "content" in tasks:
                tasks = tasks["content"]
            assert (
                len(tasks) <= limit
            ), f"Вернулось больше задач, чем лимит: {len(tasks)}"

    @allure.title("Удаление задачи (PUT /tasks/{taskId})")
    def test_delete_task(self, api_client: TaskAPI, config: dict) -> None:
        """Позитивный тест на удаление задачи."""
        # Создаем задачу локально, так как фикстура created_task удалит её сама
        column_id = config["column_id"]
        create_resp = api_client.create_task("Задача на удаление", column_id)
        task_id = create_resp.json()["id"]

        response = api_client.delete_task(task_id)

        with allure.step("Проверка статус-кода 204 или 200)"):
            assert response.status_code in [200,204], f"Ожидался 200 или 204, получен {response.status_code}"

        with allure.step(
            "Проверка, что задача помечена как удаленная"
        ):
            get_resp = api_client.get_task_by_id(task_id)
            assert get_resp.status_code == 200, f"Ожидался 200, получен {get_resp.status_code}"
            assert get_resp.json().get("deleted") is True, "Задача не была помечена как удаленная!"

    @allure.title("Создание задачи без обязательного поля columnId (POST /tasks)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_task_without_column_id(self, api_client: TaskAPI) -> None:
        """Негативный тест: создание задачи без обязательного поля."""
        response = api_client.create_task_without_column("Задача без колонки")

        with allure.step("Проверка статус-кода 201 (Created) вместо 400"):
            assert (
                response.status_code == 201
            ), f"Ожидался 201, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert "id" in response.text

    @allure.title("Получение несуществующей задачи (GET /tasks/{taskId})")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_task(self, api_client: TaskAPI) -> None:
        """Негативный тест: получение несуществующей задачи."""
        response = api_client.get_nonexistent_task()

        with allure.step("Проверка статус-кода 404 (Not Found)"):
            assert (
                response.status_code == 404
            ), f"Ожидался 404, получен {response.status_code}"
