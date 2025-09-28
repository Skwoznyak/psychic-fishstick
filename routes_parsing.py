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
)
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
import os


from auth_deps import security


router_parsing = APIRouter()


@router_parsing.post("/elama-856489 nudnoi.ru", tags=['Парсинг страницы'], dependencies=[Depends(security.access_token_required)])
def run_elama_856489(background_tasks: BackgroundTasks) -> JSONResponse:
    if not load_cookies():
        return JSONResponse(
            status_code=409,
            content={
                "message": "Нет сохранённых куки. Сначала вызовите /auth/start, войдите вручную и затем /auth/save",
            },
        )
    background_tasks.add_task(
        start_parsing_background_job_elama_856489_nudnoi_ru)
    return JSONResponse(
        status_code=202,
        content={
            "message": "Парсинг elama-856489 nudnoi.ru запущен. Проверьте результат по /download, когда задача завершится."},
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
