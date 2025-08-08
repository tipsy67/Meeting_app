import hashlib
import hmac
from urllib.parse import parse_qsl

from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

from api_app.core.config import settings
from api_app.schemas.users import UserCreateUpdate


class TelegramAuth:
    async def __call__(self, request: Request):
        body = await request.json()
        init_data = body.get("initData")
        if not init_data:
            raise HTTPException(status_code=401, detail="Missing initData")

        user_data = self.verify_telegram_data(init_data)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid Telegram auth")

        return user_data

    def verify_telegram_data(self, init_data: str) -> UserCreateUpdate|None:
        try:
            parsed_data = dict(parse_qsl(init_data))
            user_data = UserCreateUpdate(**parsed_data)
            hash_str = parsed_data.pop('hash')

            data_check_string = "\n".join(
                f"{key}={value}" for key, value in sorted(parsed_data.items())
            )

            secret_key = hashlib.sha256(settings.tg.token.encode()).digest()
            computed_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256
            ).hexdigest()

            if computed_hash == hash_str:
                return user_data
        except ValueError:
            return None