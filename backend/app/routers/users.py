from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def list_users():
    """Возвращает список пользователей"""
    return []


@router.get("/users/{user_id}", tags=["users"])
async def get_user():
    """Возвращает данные пользователя"""
    return {}


@router.post("/users/", tags=["users"])
async def create_user():
    """Создает нового пользователя"""
    return {}


@router.put("/users/{user_id}", tags=["users"])
async def update_user():
    """Обновляет данные пользователя"""
    return {}


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user():
    """Удаляет пользователя"""
    return {}
