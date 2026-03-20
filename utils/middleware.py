from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from database.crud import get_or_create_user

class UserLanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        if user:
            db_user = await get_or_create_user(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
            )
            data["lang"] = db_user.language
        else:
            data["lang"] = "ru"
        return await handler(event, data)
