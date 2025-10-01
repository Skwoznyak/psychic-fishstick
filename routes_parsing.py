from parsing import load_cookies
from services import (
    export_path,
    open_login_page,
    persist_cookies,
    start_parsing_background_job_elama_856489_nudnoi_ru,
    start_parsing_rocketcars,
    start_parsing_buycar,
    start_parsing_coffelike,
    start_parsing_panda28,
    start_parsing_buybox,
    start_parsing_colife,
    start_parsing_gepard_agency,
    start_parsing_async,
    get_parsing_status,
    get_last_parsed_file,
)
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
import os


from auth_deps import security


router_parsing = APIRouter()


@router_parsing.get("/status", tags=['Статус парсинга'], dependencies=[Depends(security.access_token_required)])
def get_parsing_status_endpoint() -> dict:
    """Возвращает текущий статус парсинга"""
    status = get_parsing_status()
    return {
        "is_running": status["is_running"],
        "progress": status["progress"],
        "last_update": status["last_update"],
        "ready_to_download": not status["is_running"] and status["progress"] == "✅ Парсинг завершён"
    }


@router_parsing.post("/elama-856489 nudnoi.ru", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
async def run_elama_856489() -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )

    # Запускаем асинхронный парсинг
    import asyncio
    asyncio.create_task(start_parsing_async())

    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг elama-856489 nudnoi.ru запущен. Проверьте статус по /parsing/status, когда задача завершится."},
    )


@router_parsing.post("/rocketcars", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_rocketcars(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_rocketcars)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг RocketCars запущен. Проверьте результат по /download, когда задача завершится.",
            "status_check": "Используйте /status для проверки готовности файла",
            "download_url": "/download"
        },
    )


@router_parsing.post("/buycar", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_buycar(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_buycar)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг BuyCar запущен. Проверьте результат по /download, когда задача завершится."},
    )


@router_parsing.post("/coffelike", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_coffelike(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_coffelike)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг Coffelike запущен. Проверьте результат по /download, когда задача завершится."},
    )


@router_parsing.post("/panda28", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_panda28(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_panda28)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг Panda 28 запущен. Проверьте результат по /download, когда задача завершится."},
    )


@router_parsing.post("/buybox", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_buybox(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_buybox)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг BuyBox запущен. Проверьте результат по /download, когда задача завершится."},
    )


@router_parsing.post("/colife", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_colife(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_colife)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг Colife Invest запущен. Проверьте результат по /download, когда задача завершится."},
    )


@router_parsing.post("/elama-379335 gepard-agency", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_gepard_agency(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(start_parsing_gepard_agency)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг elama-379335 gepard-agency запущен. Проверьте результат по /download, когда задача завершится."},
    )


@router_parsing.get("/download", tags=['Скачать таблицу'], dependencies=[Depends(security.access_token_required)])
def download_file() -> FileResponse:
    try:
        last_file = get_last_parsed_file()
        if not last_file:
            raise HTTPException(
                status_code=404,
                detail="Нет файлов для скачивания. Сначала запустите парсинг любого аккаунта"
            )
        path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), last_file)
        if not os.path.exists(path):
            raise HTTPException(
                status_code=404,
                detail=f"Файл {last_file} не найден. Возможно, парсинг еще не завершился"
            )
        return FileResponse(path, filename=last_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=403, detail="У вас нет доступов")
