import allure
import requests
from requests import Response


class TaskAPI:
    def __init__(self, base_url: str, api_key: str, company_id: str) -> None:
        self.base_url = f"{base_url}/api-v2"
        self.company_id = company_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @allure.step("API: Создание задачи с названием '{title}'")
    def create_task(self, title: str, column_id: str) -> Response:
        url = f"{self.base_url}/tasks"
        payload = {"title": title, "columnId": column_id}
        return requests.post(url, json=payload, headers=self.headers)

    @allure.step("API: Создание задачи без обязательного поля columnId")
    def create_task_without_column(self, title: str) -> Response:
        url = f"{self.base_url}/tasks"
        payload = {"title": title}
        return requests.post(url, json=payload, headers=self.headers)

    @allure.step("API: Получение задачи по ID '{task_id}'")
    def get_task_by_id(self, task_id: str) -> Response:
        url = f"{self.base_url}/tasks/{task_id}"
        return requests.get(url, headers=self.headers)

    @allure.step("API: Получение списка задач с лимитом {limit}")
    def get_tasks_with_limit(self, limit: int = 10) -> Response:
        url = f"{self.base_url}/tasks"
        params = {"limit": limit}
        return requests.get(url, headers=self.headers, params=params)

    @allure.step("API: Обновление задачи '{task_id}'")
    def update_task(self, task_id: str, new_title: str) -> Response:
        url = f"{self.base_url}/tasks/{task_id}"
        payload = {"title": new_title}
        return requests.put(url, json=payload, headers=self.headers)

    @allure.step("API: Удаление задачи '{task_id}'")
    def delete_task(self, task_id: str) -> Response:
        url = f"{self.base_url}/tasks/{task_id}"
        payload = {"deleted": True}

        response = requests.put(url, json=payload, headers=self.headers)

        return response

    @allure.step("API: Получение несуществующей задачи")
    def get_nonexistent_task(self) -> Response:
        url = f"{self.base_url}/tasks/00000000-0000-0000-0000-000000000000"
        return requests.get(url, headers=self.headers)
