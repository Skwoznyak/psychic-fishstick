import os
import time
import json
import asyncio
import threading
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor

from parsing import (
    load_cookies,
    save_cookies,
    get_driver,
    check_token_lifetime,
    parse_ads_table_to_excel,
    clic_elama_856489_nudnoi_ru,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Глобальные переменные для отслеживания статуса
parsing_status = {
    "is_running": False,
    "current_task": None,
    "progress": "Готов к запуску",
    "last_update": None
}

parsing_lock = threading.Lock()


def export_path() -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "elama-856489 nudnoi.ru.xlsx")


def save_last_parsed_file(filename: str):
    """Сохраняет информацию о последнем созданном файле"""
    timestamp = datetime.now().isoformat()
    with open("last_parsed.json", "w") as f:
        json.dump({"filename": filename, "timestamp": timestamp}, f)
    print(f"✅ [ФАЙЛ ГОТОВ] {filename} сохранен в {timestamp}")
    print(f"📁 [СКАЧИВАНИЕ] Файл готов к скачиванию по /download")


def get_last_parsed_file():
    """Получает информацию о последнем созданном файле"""
    try:
        with open("last_parsed.json", "r") as f:
            data = json.load(f)
            return data["filename"]
    except:
        return None


def open_login_page(phone: str) -> None:
    driver = get_driver()
    print(f"[АВТОРИЗАЦИЯ] 🌐 Перехожу на страницу аккаунта...")
    driver.get("https://ads.telegram.org/account")
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    wait = WebDriverWait(driver, 15)  # Увеличиваем timeout
    print(f"[АВТОРИЗАЦИЯ] ⏳ Жду загрузки страницы...")
    time.sleep(3)  # Даем время на загрузку

    # Попробовать закрыть popup клавишей ESC (на всякий случай)
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
    except Exception:
        pass

    # 1. Кликнуть по кнопке "Log in to Start Advertizing"
    # Пробуем разные селекторы для кнопки входа
    login_selectors = [
        "a.login-link",
        "a[href='/auth']",
        ".login-link",
        "a.btn.pr-btn.login-link",
        "a[class*='login']",
        "a[href*='auth']"
    ]

    login_btn = None
    for selector in login_selectors:
        try:
            print(f"[АВТОРИЗАЦИЯ] Пробую селектор: {selector}")
            login_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            print(f"[АВТОРИЗАЦИЯ] ✅ Кнопка найдена с селектором: {selector}")
            break
        except Exception as e:
            print(f"[АВТОРИЗАЦИЯ] ❌ Селектор {selector} не найден: {e}")
            continue

    if not login_btn:
        raise Exception("Кнопка входа не найдена ни с одним селектором")

    driver.execute_script("arguments[0].scrollIntoView();", login_btn)
    login_btn.click()
    time.sleep(2)

    # 2. Дождаться, когда форма send-form станет видимой (уберётся класс hide)
    try:
        print(f"[АВТОРИЗАЦИЯ] Жду появления формы входа...")
        wait.until(lambda d: "hide" not in d.find_element(
            By.ID, "send-form").get_attribute("class"))
        print(f"[АВТОРИЗАЦИЯ] ✅ Форма входа появилась")
    except Exception as e:
        print(f"[АВТОРИЗАЦИЯ] ❌ Форма входа не появилась: {e}")
        # Пробуем найти форму по альтернативным селекторам
        form_selectors = ["#send-form", ".send-form", "form", "[id*='form']"]
        for selector in form_selectors:
            try:
                form = driver.find_element(By.CSS_SELECTOR, selector)
                if form.is_displayed():
                    print(
                        f"[АВТОРИЗАЦИЯ] ✅ Форма найдена с селектором: {selector}")
                    break
            except:
                continue

    # 3. Ввести телефон
    phone_selectors = ["#phone-number", "input[type='tel']",
                       "input[placeholder*='+']", "input[name*='phone']"]
    phone_input = None

    for selector in phone_selectors:
        try:
            print(f"[АВТОРИЗАЦИЯ] Пробую найти поле телефона: {selector}")
            phone_input = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            print(
                f"[АВТОРИЗАЦИЯ] ✅ Поле телефона найдено с селектором: {selector}")
            break
        except Exception as e:
            print(f"[АВТОРИЗАЦИЯ] ❌ Селектор {selector} не найден: {e}")
            continue

    if not phone_input:
        raise Exception("Поле ввода телефона не найдено")

    phone_input.clear()
    phone_input.send_keys(phone)
    print(f"[АВТОРИЗАЦИЯ] ✅ Номер телефона введен: {phone}")
    time.sleep(1)

    # 4. Кликнуть по кнопку "Next" внутри формы send-form
    next_selectors = [
        "button[type='submit'].btn-link.btn-lg",
        "button[type='submit']",
        "button.btn-link.btn-lg",
        "button:contains('Next')",
        "input[type='submit']",
        "button[class*='btn']"
    ]

    next_btn = None
    for selector in next_selectors:
        try:
            print(f"[АВТОРИЗАЦИЯ] Пробую найти кнопку Next: {selector}")
            next_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)))
            print(
                f"[АВТОРИЗАЦИЯ] ✅ Кнопка Next найдена с селектором: {selector}")
            break
        except Exception as e:
            print(f"[АВТОРИЗАЦИЯ] ❌ Селектор {selector} не найден: {e}")
            continue

    if not next_btn:
        raise Exception("Кнопка Next не найдена")

    next_btn.click()
    print(f"[АВТОРИЗАЦИЯ] ✅ Кнопка Next нажата")
    time.sleep(2)


def persist_cookies() -> None:
    try:
        save_cookies()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Не удалось сохранить куки: {e}")


def update_parsing_status(progress: str, is_running: bool = None):
    """Обновляет статус парсинга"""
    with parsing_lock:
        global parsing_status
        parsing_status["progress"] = progress
        parsing_status["last_update"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        if is_running is not None:
            parsing_status["is_running"] = is_running
        print(f"📊 [СТАТУС] {progress}")


def start_parsing_background_job_elama_856489_nudnoi_ru() -> None:
    try:
        update_parsing_status("🚀 Начало парсинга elama-856489 nudnoi.ru", True)
        print(
            f"🚀 [{datetime.now().strftime('%H:%M:%S')}] Начало парсинга elama-856489 nudnoi.ru")

        update_parsing_status("🔐 Загружаю куки...")
        print("🔐 [АВТОРИЗАЦИЯ] Загружаю куки...")
        if not load_cookies():
            update_parsing_status("❌ Нет сохраненных куки", False)
            print("❌ [ОШИБКА] Нет сохраненных куки")
            return

        update_parsing_status("🌐 Получаю драйвер...")
        print("🌐 [БРАУЗЕР] Получаю драйвер...")
        driver = get_driver()

        update_parsing_status("🌐 Перехожу на страницу аккаунта...")
        print("🌐 [БРАУЗЕР] Перехожу на страницу аккаунта...")
        driver.get("https://ads.telegram.org/account")

        update_parsing_status("⏳ Жду загрузки страницы...")
        print("⏳ [ОЖИДАНИЕ] Жду загрузки страницы...")
        time.sleep(3)

        # Автоклик по кнопке, содержащей точный текст "elama-856489 nudnoi.ru"
        update_parsing_status("🎯 Ищу кнопку аккаунта...")
        try:
            clic_elama_856489_nudnoi_ru("elama-856489 nudnoi.ru", timeout=60)
            update_parsing_status("✅ Кнопка найдена и нажата")
            print("✅ [КЛИК] Кнопка найдена и нажата")
        except Exception as e:
            update_parsing_status(f"❌ Не удалось найти кнопку: {e}")
            print(f"❌ [ОШИБКА] Не удалось найти кнопку: {e}")

        update_parsing_status("⏰ Проверяю время жизни токена...")
        print("⏰ [ПРОВЕРКА] Проверяю время жизни токена...")
        check_token_lifetime()

        update_parsing_status("📊 Начинаю парсинг данных...")
        print("📊 [ПАРСИНГ] Начинаю парсинг данных...")
        filename = "elama-856489 nudnoi.ru.xlsx"
        parse_ads_table_to_excel(filename)

        update_parsing_status("💾 Сохраняю файл...")
        save_last_parsed_file(filename)

        update_parsing_status("✅ Парсинг завершён", False)
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Парсинг завершён")

    except Exception as e:
        update_parsing_status(f"❌ Критическая ошибка: {e}", False)
        print(f"❌ [КРИТИЧЕСКАЯ ОШИБКА] {e}")
        import traceback
        print(f"❌ [СТЕК ТРЕЙС] {traceback.format_exc()}")
        # Сохраняем файл с ошибкой
        try:
            filename = "elama-856489 nudnoi.ru.xlsx"
            import pandas as pd
            df = pd.DataFrame([], columns=["Ошибка"])
            df.loc[0] = f"Ошибка парсинга: {str(e)}"

            # Добавляем время ошибки с часовым поясом
            import pytz
            try:
                moscow_tz = pytz.timezone('Europe/Moscow')
                local_time = datetime.now(moscow_tz)
                df['Время ошибки'] = local_time.strftime(
                    "%Y-%m-%d %H:%M:%S MSK")
            except:
                df['Время ошибки'] = datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M:%S UTC")
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Ошибка', index=False)
            save_last_parsed_file(filename)
        except:
            pass


async def start_parsing_async():
    """Асинхронная версия парсинга"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, start_parsing_background_job_elama_856489_nudnoi_ru)


def _start_parsing_generic(account_title: str, filename: str) -> None:
    """Общий парсер: кликает по аккаунту с именем account_title и сохраняет в filename."""
    update_parsing_status(f"🚀 Начало парсинга {account_title}", True)
    if not load_cookies():
        update_parsing_status("❌ Нет сохраненных куки", False)
        return

    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    update_parsing_status("🎯 Ищу кнопку аккаунта...")
    try:
        clic_elama_856489_nudnoi_ru(account_title, timeout=60)
        update_parsing_status("✅ Кнопка найдена и нажата")
    except Exception as e:
        update_parsing_status(f"❌ Не удалось найти кнопку: {e}")

    update_parsing_status("⏰ Проверяю время жизни токена...")
    check_token_lifetime()

    update_parsing_status("📊 Начинаю парсинг данных...")
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)
    update_parsing_status("✅ Парсинг завершён", False)


def start_parsing_gepard_agency() -> None:
    """Парсинг для elama-379335 gepard-agency"""
    _start_parsing_generic("elama-379335 gepard-agency",
                           "gepard-agency_export.xlsx")


def get_parsing_status():
    """Возвращает текущий статус парсинга"""
    with parsing_lock:
        return parsing_status.copy()


def start_parsing_rocketcars() -> None:
    """Парсинг для RocketCars - elama-249960 RocketCarsMSK"""
    print(f"🚀 [{datetime.now().strftime('%H:%M:%S')}] Начало парсинга RocketCars")
    if not load_cookies():
        print("❌ [ОШИБКА] Нет сохраненных куки")
        return

    print("🔐 [АВТОРИЗАЦИЯ] Загружаю куки...")
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    print("🎯 [КЛИК] Ищу кнопку 'elama-249960 RocketCarsMSK'...")
    try:
        clic_elama_856489_nudnoi_ru("elama-249960 RocketCarsMSK", timeout=60)
        print("✅ [КЛИК] Кнопка найдена и нажата")
    except Exception as e:
        print(f"❌ [ОШИБКА] Не удалось найти кнопку: {e}")

    print("⏰ [ПРОВЕРКА] Проверяю время жизни токена...")
    check_token_lifetime()

    print("📊 [ПАРСИНГ] Начинаю парсинг данных...")
    filename = "rocketcars_export.xlsx"
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)


def start_parsing_buycar() -> None:
    """Парсинг для BuyCar - Telescope / buycar_with_uss // CR_Telegram Ads"""
    print(f"🚀 [{datetime.now().strftime('%H:%M:%S')}] Начало парсинга BuyCar")
    if not load_cookies():
        print("❌ [ОШИБКА] Нет сохраненных куки")
        return

    print("🔐 [АВТОРИЗАЦИЯ] Загружаю куки...")
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    print("🎯 [КЛИК] Ищу кнопку 'Telescope / buycar_with_uss // CR_Telegram Ads'...")
    try:
        clic_elama_856489_nudnoi_ru(
            "Telescope / buycar_with_uss // CR_Telegram Ads", timeout=60)
        print("✅ [КЛИК] Кнопка найдена и нажата")
    except Exception as e:
        print(f"❌ [ОШИБКА] Не удалось найти кнопку: {e}")

    print("⏰ [ПРОВЕРКА] Проверяю время жизни токена...")
    check_token_lifetime()

    print("📊 [ПАРСИНГ] Начинаю парсинг данных...")
    filename = "buycar_export.xlsx"
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)


def start_parsing_coffelike() -> None:
    """Парсинг для Coffelike - elama-126515 on_tcscoffee"""
    print(f"[{datetime.now()}] Начало парсинга Coffelike")
    if not load_cookies():
        return
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    try:
        clic_elama_856489_nudnoi_ru("elama-126515 on_tcscoffee", timeout=60)
    except Exception:
        pass

    check_token_lifetime()
    filename = "coffelike_export.xlsx"
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)
    print(f"[{datetime.now()}] Файл {filename} создан")


def start_parsing_panda28() -> None:
    """Парсинг для Panda 28 - Telescope_SS_CR / panda_cargo_28_premium / O / 15840"""
    print(f"[{datetime.now()}] Начало парсинга Panda 28")
    if not load_cookies():
        return
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    try:
        clic_elama_856489_nudnoi_ru(
            "Telescope_SS_CR / panda_cargo_28_premium / O / 15840", timeout=60)
    except Exception:
        pass

    check_token_lifetime()
    filename = "panda28_export.xlsx"
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)
    print(f"[{datetime.now()}] Файл {filename} создан")


def start_parsing_buybox() -> None:
    """Парсинг для BuyBox - Telescope_SS_CR / BuyBox_China_premium / O / 15339"""
    print(f"[{datetime.now()}] Начало парсинга BuyBox")
    if not load_cookies():
        return
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    try:
        clic_elama_856489_nudnoi_ru(
            "Telescope_SS_CR / BuyBox_China_premium / O / 15339", timeout=60)
    except Exception:
        pass

    check_token_lifetime()
    filename = "buybox_export.xlsx"
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)
    print(f"[{datetime.now()}] Файл {filename} создан")


def start_parsing_colife() -> None:
    """Парсинг для Colife Invest - elama-489613 investcolife RE"""
    print(f"[{datetime.now()}] Начало парсинга Colife Invest")
    if not load_cookies():
        return
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    try:
        clic_elama_856489_nudnoi_ru("elama-489613 investcolife RE", timeout=60)
    except Exception:
        pass

    check_token_lifetime()
    filename = "colife_export.xlsx"
    parse_ads_table_to_excel(filename)
    save_last_parsed_file(filename)
    print(f"[{datetime.now()}] Файл {filename} создан")
