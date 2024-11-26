from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import OperationCreate
from ..database import get_async_session
from .models import operation

router = APIRouter(
    prefix="/operations",
    tags=["Operation"],
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    # конструкция ниже не работает, result.all() - возвращает кортеж без названий столбцов
    # (получаю список кортежей, а не список словарей - возможно, где то его отдельно надо делать),
    # соответственно получаю ошибку, что словарь не может быть сформирован!
    return result.all()

# async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
#     # query - обычно это запрос на выборку (select)
#     # statement (сокращенно stmt) - обычно запросы на удаление, вставку
#     # where (где) - условие
#     query = select(operation).where(operation.c.type == operation_type)
#     # operation.c.type - в таблице operation обращаемся к столбцу type
#     result = await session.execute(query)
#     # execute - применить команду
#     return result.all()
#     # Функцией all() забираем данные

# Запрос на добавление строк
@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmp = insert(operation).values(**new_operation.dict())
    # В values должен быть словарь, к примеру: values(id=1, figi="awrq"). И для разворачивания
    # модели экземпляра класса pydentic в **kwargs - необходимо создать словарь - делаем через *.dict()
    # ** - разворачиваем словарь
    # далее задействуем сессию и выполняем код stmt:
    await session.execute(stmp)
    # На этом шаге ничего не исполниться. Мы находимся внутри транзакции, и для её исполнения необходимо прописать commit():
    await session.commit()
    # смысл - может быть несколько операций, и часть может не выполниться - поэтому после корректного исполнения всех,
    # делается commit() - и заносятся все операции.
    return {"status": "success"}


# ORM - Object-relational model - Объектно реляционная модель (перенос объектов из Python в БД):
# Концепция работы с базой данных (реляционная).
# Объект - что то в языке программирования - экземпляр класса (у нас User класс имеется).
# И объекты отображают что-то, что имеется в БД.

# SQL инъекции - можно вставить свой код в запрос - вызвав негативное поведение
# ORM позволяет составлять запросы так, чтобы не было возможности вставить в запрос ещё и иные команды к БД.

# SQLAlchemy позволяет нам конструировать запросы, а реализацию запроса выполняет драйвер
# asyncpg например.