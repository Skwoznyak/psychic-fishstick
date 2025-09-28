from services import (
    export_path,
    open_login_page,
    persist_cookies,
    get_last_parsed_file,
)
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Body
from fastapi.responses import FileResponse, JSONResponse
import os


from auth_deps import security


router = APIRouter()


@router.get('/')
def root() -> dict:
    return {"message": "Welcome to my API"}


@router.post("/auth/start", tags=['Авторизация'], dependencies=[Depends(security.access_token_required)])
def auth_start(phone: str = Body(..., embed=True)) -> dict:
    open_login_page(phone)
    return {
        "message": "Номер телефона отправлен. Дальнейшие шаги (код из Telegram) нужно реализовать отдельно.",
    }


@router.post("/auth/save", tags=['Авторизация'], dependencies=[Depends(security.access_token_required)])
def auth_save() -> dict:
    persist_cookies()
    return {"message": "Куки сохранены"}


@router.get("/status", tags=['Статус парсинга'], dependencies=[Depends(security.access_token_required)])
def get_parsing_status() -> dict:
    """Проверяет статус последнего парсинга"""
    try:
        last_file = get_last_parsed_file()
        if not last_file:
            return {
                "status": "no_files",
                "message": "Нет файлов для скачивания. Сначала запустите парсинг любого аккаунта",
                "last_file": None,
                "ready_to_download": False
            }

        path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), last_file)
        file_exists = os.path.exists(path)

        return {
            "status": "ready" if file_exists else "processing",
            "message": f"Файл {last_file} {'готов к скачиванию' if file_exists else 'еще обрабатывается'}",
            "last_file": last_file,
            "ready_to_download": file_exists,
            "file_path": path if file_exists else None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка при проверке статуса: {str(e)}",
            "last_file": None,
            "ready_to_download": False
        }


@router.get("/download", tags=['Скачать таблицу'], dependencies=[Depends(security.access_token_required)])
def download() -> FileResponse:
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


# @router.get('/protected', dependencies=[Depends(security.access_token_required)])
# # def protected():
# #     try:
# #         return {'data':'TOP SECRET'}
# #     except Exception:
# #         raise HTTPException(status_code=403, detail="У вас нет доступов")
