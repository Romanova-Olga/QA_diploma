import allure
from playwright.sync_api import Page
from base_page import BasePage


class MessengerPage(BasePage):
    def __init__(self, page: Page, company_id: str) -> None:
        super().__init__(page)
        self.company_id = company_id
        self.new_chat_btn = page.locator('[data-testid="create-chat-menu-trigger"]') 
        self.search_input = page.get_by_placeholder("Поиск").first
        self.message_input = page.locator('#chat-item-editor [contenteditable="true"]')
        self.send_btn = page.locator('[data-icon="IconSend"]')

    @allure.step("Открытие окна нового чата и поиск пользователя '{recipient}'")
    def open_new_chat_and_search(self, recipient: str) -> None:
    # 1. Переходим на страницу команды
        self.page.goto(f"https://ru.yougile.com/team/{self.company_id}/")
    
        # 2. Кликаем по "Мессенджер" в левом меню
        self.page.locator("text=Мессенджер").last.click()
    
        # 3. Ждем загрузки страницы мессенджера
        self.page.wait_for_timeout(2000)
    
        # 4. Кликаем по кнопке создания чата (плюсик)
        self.new_chat_btn.click()
    
        # 5. Вводим имя пользователя в поиск (он его не найдёт)
        self.search_input.fill(recipient)
    
        # 6. Небольшая пауза, чтобы система успела показать результат поиска
        self.page.wait_for_timeout(1000)

    def is_user_not_found_visible(self) -> bool:
        """Проверяет, отображается ли сообщение 'Не найдено' при поиске."""
        # Ищем текст "Не найдено"
        return self.page.get_by_text("Не найдено").is_visible()

    @allure.step("Создание группового чата: {group_name}")
    def create_group_chat(self, group_name: str, members: list[str]) -> None:
        # 1. Переходим на страницу команды
        self.page.goto(f"https://ru.yougile.com/team/{self.company_id}/")
    
        # 2. Кликаем по "Мессенджер"
        self.page.locator("text=Мессенджер").last.click()
    
        # 3. Ждем загрузки
        self.page.wait_for_timeout(2000)
    
        # 4. Кликаем по кнопке создания чата
        self.new_chat_btn.click()
    
        # 5. Выбираем "Создать групповой чат"
        self.page.get_by_text("Создать групповой чат").click()

        # 6. Ждем пока появится поле для ввода названия
        self.page.wait_for_selector("input[placeholder='Введите название группового чата']",timeout=10000)
    
        # 7. Заполняем название группы
        self.page.get_by_placeholder("Введите название группового чата").fill(group_name)
        
        # 9. Нажимаем кнопку "Создать чат"
        self.page.get_by_role("button", name="Создать чат").click()

    def is_group_chat_created(self, group_name: str) -> bool:
        return self.page.get_by_text(group_name).first.is_visible()
