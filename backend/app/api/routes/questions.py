from fastapi import APIRouter

router = APIRouter()


@router.get("/questions/", tags=["questions"])
async def list_questions():
    """Возвращает список вопросов"""
    return []


@router.get("/questions/{question_id}", tags=["questions"])
async def get_question():
    """Возвращает данные вопроса"""
    return {}


@router.post("/questions/", tags=["questions"])
async def create_question():
    """Создает новый вопрос"""
    return {}


@router.put("/questions/{question_id}", tags=["questions"])
async def update_question():
    """Обновляет данные вопроса"""
    return {}


@router.delete("/questions/{question_id}", tags=["questions"])
async def delete_question():
    """Удаляет вопрос"""
    return {}
