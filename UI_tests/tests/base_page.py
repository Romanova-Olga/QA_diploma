import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Переход по URL: {url}")
    def navigate(self, url: str) -> None:
        self.page.goto(url)
