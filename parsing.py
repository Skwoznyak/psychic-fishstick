from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
import time
import csv
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service

# Ленивая инициализация драйвера, чтобы он не создавался на импорт модуля
driver = None


def get_driver():
    global driver
    if driver is None:
        # ⚙️ НАСТРОЙКА БРАУЗЕРА
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/chromium"
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# 📁 ФАЙЛ ДЛЯ СОХРАНЕНИЯ КУК
COOKIES_FILE = "cookies_for_max.pkl"


def manual_login():
    """Ручная авторизация пользователем"""
    driver = get_driver()
    print("🔐 НУЖНА РУЧНАЯ АВТОРИЗАЦИЯ")
    print("1. Браузер откроет страницу сайт")
    print("2. Войдите в свой аккаунт")
    print("3. После успешного входа нажмите Enter здесь в консоли")
    print("=" * 50)

    # Открываем сайт для ручного входа
    driver.get("https://ads.telegram.org/account")
    time.sleep(2)

    # Ждем, пока пользователь вручную авторизуется
    input("После успешного входа нажмите Enter чтобы продолжить...")

    # Сохраняем куки после авторизации
    save_cookies()

    print("✅ Авторизация завершена! Куки сохранены.")
    return True


def save_cookies():
    """Сохраняет куки в файл"""
    driver = get_driver()
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, 'wb') as file:
        pickle.dump(cookies, file)
    print("💾 Куки сохранены в файл")


def load_cookies():
    """Загружает куки из файла"""
    driver = get_driver()
    if os.path.exists(COOKIES_FILE):
        driver.get("https://ads.telegram.org/account")
        time.sleep(2)

        with open(COOKIES_FILE, 'rb') as file:
            cookies = pickle.load(file)

            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    continue

        print("✅ Куки загружены!")
        return True
    else:
        print("❌ Файл с куками не найден!")
        return False


def main():
    """Точка входа: загружаем куки или просим ручной логин и держим окно открытым."""
    driver = get_driver()
    # Сначала пробуем загрузить куки; если их нет — просим ручной вход
    logged_in = load_cookies()
    if not logged_in:
        manual_login()

    # После успешной авторизации переходим в кабинет
    driver.get("https://ads.telegram.org/account")

    # Ждём загрузки страницы
    time.sleep(3)

    # Автоклик по кнопке с подстрокой "elama-856489 nudnoi.ru", чтобы открыть таблицу объявлений
    try:
        clic_elama_856489_nudnoi_ru("elama-856489 nudnoi.ru", timeout=60)
    except Exception:
        pass

    # Парсим таблицу объявлений и сохраняем в CSV
    export_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "elama-856489 nudnoi.ru.xlsx")
    check_token_lifetime()
    parse_ads_table_to_excel(export_path)
    print(f"\n✅ Таблица объявлений сохранена: {export_path}")
    print("\n✅ Готово. Окно оставлено открытым. Закройте его вручную, когда закончите.")
    print(f"[ФАЙЛ ГОТОВ] {export_path} готов и можно скачивать.")
    # Держим скрипт активным, чтобы окно не закрывалось
    try:
        input("Нажмите Enter в консоли, чтобы закрыть драйвер и завершить скрипт...")
    finally:
        # Если хотите, чтобы браузер оставался открытым после выхода из скрипта,
        # можно закомментировать следующую строку (detach уже включён выше).
        driver.quit()


def click_account_button(account_title: str, timeout: int = 30) -> None:
    """Ожидает и нажимает на кнопку аккаунта по видимому заголовку.

    Пример искомого блока:
    <div class="pr-account-button-content">
      <div class="pr-account-button-title">elama-856489 nudnoi.ru</div>
      <div class="pr-account-button-desc">Organization</div>
    </div>
    """
    driver = get_driver()
    wait = WebDriverWait(driver, timeout)

    # Сначала показываем все доступные аккаунты для отладки
    try:
        print("📋 Ищем все доступные аккаунты...")
        accounts = driver.find_elements(
            By.CSS_SELECTOR, ".pr-account-button-title")
        print(f"Найдено аккаунтов: {len(accounts)}")
        for i, acc in enumerate(accounts):
            print(f"  {i+1}. '{acc.text}'")
    except Exception as e:
        print(f"❌ Ошибка при поиске аккаунтов: {e}")
        return

    # Ждём появления нужной кнопки аккаунта
    xpath = (
        "//div[contains(@class,'pr-account-button-content') and .//div[contains(@class,'pr-account-button-title') and normalize-space(text())=\""
        + account_title
        + "\"]]"
    )
    try:
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
        print(f"✅ Кликнули по аккаунту: {account_title}")

        # После клика ждём появления таблицы объявлений
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".js-ads-table-body tr")))
    except Exception as e:
        print(f"❌ Не удалось найти аккаунт '{account_title}': {e}")
        print("💡 Скопируйте точное название из списка выше и замените в коде")


def clic_elama_856489_nudnoi_ru(substring: str, timeout: int = 30) -> None:
    """Кликает по аккаунту на странице выбора аккаунта.

    Ищет ссылки-кнопки `a.pr-account-button-wrap` и кликает ту, чей текст
    содержит указанную подстроку (без учёта регистра). После клика ждёт
    появления строк таблицы объявлений.
    """
    driver = get_driver()
    wait = WebDriverWait(driver, timeout)

    try:
        # Ждём появления списка аккаунтов на странице выбора
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.pr-account-button-wrap")))
        buttons = driver.find_elements(
            By.CSS_SELECTOR, "a.pr-account-button-wrap")
        needle = substring.strip().lower()

        target = None
        for btn in buttons:
            try:
                full_text = btn.text.strip().lower()
                if needle in full_text:
                    target = btn
                    break
            except Exception:
                continue

        if not target:
            raise Exception(
                f"Кнопка с подстрокой '{substring}' не найдена среди a.pr-account-button-wrap")

        # Клик по самой ссылке
        target.click()
        print(f"✅ Клик по аккаунту (подстрока): {substring}")

        # Ожидаем появления таблицы объявлений на странице аккаунта
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".js-ads-table-body tr")))
    except Exception as e:
        print(f"❌ Не удалось кликнуть по подстроке '{substring}': {e}")


def _safe_text(elem):
    """Возвращает текст элемента, если он есть, иначе пустую строку."""
    try:
        if elem is None:
            return ""
        return elem.text.strip()
    except Exception:
        return ""


def check_token_lifetime() -> None:
    """Проверяет время жизни токена и предупреждает о скором истечении"""
    driver = get_driver()
    try:
        # Ищем информацию о токене на странице
        token_info = driver.find_elements(
            By.XPATH, "//*[contains(text(), 'token') or contains(text(), 'Token') or contains(text(), 'токен')]")

        # Проверяем куки на предмет времени истечения
        cookies = driver.get_cookies()
        for cookie in cookies:
            if 'stel_dt' in cookie.get('name', '').lower() or 'token' in cookie.get('name', '').lower():
                if 'expiry' in cookie:
                    expiry_time = datetime.fromtimestamp(cookie['expiry'])
                    time_left = expiry_time - datetime.now()

                    if time_left.total_seconds() < 3600:  # Меньше часа
                        print(f"⚠️ ВНИМАНИЕ: Токен истекает через {time_left}")
                    elif time_left.total_seconds() < 86400:  # Меньше дня
                        print(f"⚠️ Токен истекает через {time_left}")
                    else:
                        print(
                            f"✅ Токен действителен ещё {time_left.days} дней")
                    return

        print("ℹ️ Информация о времени жизни токена не найдена")
    except Exception as e:
        print(f"❌ Ошибка при проверке токена: {e}")


def parse_ads_table_to_excel(excel_path: str, timeout: int = 30) -> None:
    """Парсит таблицу объявлений на странице аккаунта и сохраняет в Excel."""
    driver = get_driver()
    wait = WebDriverWait(driver, timeout)

    print(f"[ПАРСИНГ] Жду появления таблицы объявлений...")
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".js-ads-table-body")))

    # Получаем количество строк
    rows_count = len(driver.find_elements(
        By.CSS_SELECTOR, ".js-ads-table-body tr"))
    print(f"[ПАРСИНГ] Найдено строк в таблице: {rows_count}")

    # Заголовки
    headers = [
        "Ad Title", "URL", "Views", "Opened", "Clicks", "Actions",
        "CTR", "CVR", "CPM", "CPC", "CPA", "Spent", "Budget", "Target", "Status", "Date Added",
    ]

    data_rows: list[list[str]] = []

    # Итерируемся по индексам, а не по элементам
    for i in range(rows_count):
        try:
            # Каждый раз ищем строку заново
            rows = driver.find_elements(
                By.CSS_SELECTOR, ".js-ads-table-body tr")
            if i >= len(rows):
                break
            r = rows[i]

            tds = r.find_elements(By.CSS_SELECTOR, "td")
            if not tds:
                continue

            # 1) Первая ячейка: заголовок и URL
            title_cell = tds[0]
            title_link = None
            url_link = None
            try:
                title_link = title_cell.find_element(
                    By.CSS_SELECTOR, ".pr-cell-title a.pr-link")
            except Exception:
                title_link = None
            try:
                url_link = title_cell.find_element(
                    By.CSS_SELECTOR, "small a[target='_blank']")
            except Exception:
                url_link = None

            ad_title = _safe_text(title_link)
            ad_url = _safe_text(url_link)

            # Далее ячейки идут по порядку как в шапке
            def cell_text(idx: int) -> str:
                try:
                    cell = tds[idx]
                    link = None
                    try:
                        link = cell.find_element(By.CSS_SELECTOR, "a.pr-link")
                    except Exception:
                        link = None
                    text = _safe_text(link) or _safe_text(cell)
                    return text.replace("\n", " ").strip()
                except Exception:
                    return ""

            # Индексация: [0] уже использовали под заголовок/URL
            views = cell_text(1)
            opened = cell_text(2)
            clicks = cell_text(3)
            actions = cell_text(4)
            ctr = cell_text(5)
            cvr = cell_text(6)
            cpm = cell_text(7)
            cpc = cell_text(8)
            cpa = cell_text(9)
            spent = cell_text(10)
            budget = cell_text(11)
            target = cell_text(12)
            status = cell_text(13)
            date_added = cell_text(14)

            data_rows.append([
                ad_title, ad_url, views, opened, clicks, actions,
                ctr, cvr, cpm, cpc, cpa, spent, budget, target, status, date_added,
            ])

        except Exception as e:
            print(f"[ПАРСИНГ] Ошибка при парсинге строки {i}: {e}")
            continue

    # Создаём DataFrame и сохраняем в Excel
    df = pd.DataFrame(data_rows, columns=headers)
    df['Экспорт выполнен'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Объявления', index=False)

        # Получаем объект рабочего листа для форматирования
        worksheet = writer.sheets['Объявления']

        # Автоподбор ширины колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Максимум 50 символов
            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"[ФАЙЛ ГОТОВ] {excel_path} готов и можно скачивать.")
    print(
        f"[ПАРСИНГ] Файл {excel_path} существует: {os.path.exists(excel_path)}")


if __name__ == "__main__":
    main()
