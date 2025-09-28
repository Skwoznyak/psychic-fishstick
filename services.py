import os
import time
import json
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from parsing import (
    load_cookies,
    save_cookies,
    get_driver,
    check_token_lifetime,
    parse_ads_table_to_excel,
    clic_elama_856489_nudnoi_ru,
)


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


def open_login_page() -> None:
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(2)


def persist_cookies() -> None:
    try:
        save_cookies()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Не удалось сохранить куки: {e}")


def start_parsing_background_job_elama_856489_nudnoi_ru() -> None:
    if not load_cookies():
        return
    driver = get_driver()
    driver.get("https://ads.telegram.org/account")
    time.sleep(3)

    # Автоклик по кнопке, содержащей точный текст "elama-856489 nudnoi.ru"
    try:
        clic_elama_856489_nudnoi_ru("elama-856489 nudnoi.ru", timeout=60)
    except Exception:
        pass

    check_token_lifetime()
    parse_ads_table_to_excel(export_path())


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
