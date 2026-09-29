import allure
from playwright.sync_api import Page
from base_page import BasePage

class KanbanPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.company_id = company_id
        
        # 1. Кнопка "Добавить задачу" (ищем по тексту, так как это span внутри div)
        self.add_task_btn = page.get_by_text("Добавить задачу").first
        
        # 2. Поле ввода названия задачи (используем надежный data-testid!)
        self.task_title_input = page.locator('[data-testid="board-task-input-name"]')

    @allure.step("Создание задачи с названием: {title}")
    def create_task(self, title: str) -> None:
        # 1. Переходим на страницу команды
        self.page.goto(f"https://ru.yougile.com/team/{self.company_id}/")

        # 2. Кликаем по названию проекта в левом меню
        # ВАЖНО: Для доски Канбан мы используем проект "Дипломная работа"
        with allure.step("Клик по проекту 'Дипломная работа'"):
            self.page.get_by_text("Дипломная работа").first.click()

        # 3. Ждем загрузки доски (ждем появления кнопки "Добавить задачу")
        with allure.step("Ожидание загрузки канбан-доски"):
            self.page.wait_for_selector("text=Добавить задачу", timeout=10000)

        # 4. Нажимаем "Добавить задачу" и вводим текст
        with allure.step(f"Ввод названия задачи: '{title}'"):
            self.add_task_btn.click()

            self.page.wait_for_selector('[data-testid="board-task-input-name"]', timeout=5000)

            self.task_title_input.fill(title)
            self.task_title_input.press ("Enter")

            self.page.wait_for_selector(f"text={title}", timeout=10000)

    def is_task_visible(self, title: str) -> bool:
        # Проверяем, появилась ли задача на доске
        return self.page.get_by_text(title).first.is_visible()
