from functools import wraps
from typing import Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.base.base_service import BaseService

class Transactional:
    """
    서비스 클래스 내 함수의 decorator로 사용하여
    transaction 수행을 보장합니다.
    """
    def __call__(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 서비스 클래스의 첫 번째 인자가 self라고 가정한다.
            self: BaseService = args[0]
            session: AsyncSession = self.db
            
            async with session.begin():
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    raise e
        return wrapper