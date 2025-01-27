from functools import wraps
from typing import Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.base.base_service import BaseService

class Transactional:
    def __call__(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 서비스 클래스의 첫 번째 인자가 self라고 가정
            self: BaseService = args[0]
            session: AsyncSession = self.db
            
            async with session.begin():
                try:
                    result = await func(*args, **kwargs)
                    # 커밋은 'session.begin()' 컨텍스트 매니저가 자동으로 처리
                    return result
                except Exception as e:
                    # 롤백은 'session.begin()' 컨텍스트 매니저가 자동으로 처리
                    raise e
        return wrapper