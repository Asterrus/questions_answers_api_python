from fastapi import APIRouter

router = APIRouter()


@router.get("/answers/", tags=["answers"])
async def list_answers():
    """Возвращает список ответов"""
    return []


@router.get("/answers/{answer_id}", tags=["answers"])
async def get_answer():
    """Возвращает данные ответа"""
    return {}


@router.post("/answers/", tags=["answers"])
async def create_answer():
    """Создает новый ответ"""
    return {}


@router.put("/answers/{answer_id}", tags=["answers"])
async def update_answer():
    """Обновляет данные ответа"""
    return {}


@router.delete("/answers/{answer_id}", tags=["answers"])
async def delete_answer():
    """Удаляет ответ"""
    return {}
