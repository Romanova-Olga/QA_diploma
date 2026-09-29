import allure
from playwright.sync_api import Page
from base_page import BasePage


class SalesFunnelPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.company_id = company_id

        self.add_deal_btn = page.get_by_text("Добавить сделку").first
        self.deal_name_input = page.get_by_placeholder("Введите название").first
        self.amount_input = page.get_by_placeholder("Введите сумму").first

    @allure.step("Создание сделки '{name}' на сумму {amount}")
    def create_deal(self, name: str, amount: str) -> None:
        # 1. Переходим на страницу команды
        self.page.goto(f"https://ru.yougile.com/team/{self.company_id}/")
    
        # 2. Кликаем по названию проекта в левом меню
        # (Убедитесь, что название проекта точно "тест CRM")
        self.page.get_by_text("тест CRM").first.click()
    
        # 3. Ждем загрузки страницы
        self.page.wait_for_timeout(2000)
    
        # 4. Кликаем по кнопке "Добавить сделку"
        self.add_deal_btn.click()

        # 5. Ждем появления полей в модальном окне
        self.page.wait_for_selector("input[placeholder='Введите название']",timeout=10000)
    
        # 6. Заполняем поля
        self.deal_name_input.fill(name)
        self.amount_input.fill(amount)

        # 7. Заполняем поле "Контактное лицо" (или "Ведите имя"), чтобы активировать кнопку "Добавить"
        self.page.get_by_placeholder("Введите имя").first.fill("Ольга")
    
        # 8. Нажимаем кнопку "Добавить"
        self.page.get_by_role("button", name="Добавить").last.click()

        # 9. Ждем , пока модальное окно закроется.
        self.page.wait_for_selector("input[placeholder='Введите название']",state="hidden",timeout=10000)

        # 10. Ждем появления сделки на доске
        self.page.wait_for_selector(f"text={name}",timeout=10000)

    def is_deal_in_funnel(self, name: str) -> bool:
        return self.page.get_by_text(name).first.is_visible()
