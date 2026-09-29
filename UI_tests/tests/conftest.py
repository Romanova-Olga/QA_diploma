import pytest
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Generator, Iterator

# Путь к файлу конфигурации
CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.json"

@pytest.fixture(scope="session")
def config() -> dict:
    """Загружает конфигурацию."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    """Запуск браузера."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Оставляем видимым для отладки
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def auth_context(browser_instance: Browser, config: dict) -> Iterator[BrowserContext]:
    """
    Создает контекст с авторизацией.
    Выполняет вход и сохраняет состояние.
    """
    context = browser_instance.new_context()
    page = context.new_page()
    
    # 1. Переходим на главную
    page.goto(config["base_url"])
    
    # 2. Кликаем "Войти"
    page.get_by_role("button", name="Войти").click()
    page.wait_for_url("**/team/**")
    
    # 3. Заполняем Email и Пароль
    page.get_by_placeholder("example@mail.ru").fill(config.get("email", "romiolemarak@gmail.com"))
    page.get_by_placeholder("Пароль").fill(config["password"])
    
    # 4. Кликаем "Войти" на форме
    page.get_by_role("button", name="Войти").click()
    
    # 5. ЖДЕМ загрузки рабочего стола (это критически важно!)
    # Ждем, пока появится текст "Мой профиль"
    page.wait_for_selector("text=Мой профиль", timeout=30000)
    
    # 6. Сохраняем состояние авторизации
    context.storage_state(path="auth_state.json")
    page.close()
    
    # 7. Передаем контекст в тесты
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(auth_context: BrowserContext) -> Iterator[Page]:
    """Создает новую страницу для каждого теста."""
    page = auth_context.new_page()
    page.set_default_timeout(15000)
    yield page
    page.close()
