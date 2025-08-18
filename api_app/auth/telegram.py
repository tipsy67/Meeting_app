import hashlib
import hmac
from operator import itemgetter
from urllib.parse import parse_qsl

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from orjson import orjson

from api_app.core.config import settings
from api_app.schemas.users import UserCreateUpdate


class TelegramAuth(HTTPBearer):
    async def __call__(self, request: Request):
        content_type = request.headers.get("content-type", "")

        if "application/json" not in content_type:
            raise HTTPException(
                status_code=400, detail="Content-Type must be application/json"
            )

        body = await request.json()
        init_data = body.get("initData")
        if not init_data:
            raise HTTPException(status_code=401, detail="Missing initData")

        user_data = self.verify_telegram_data(init_data)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid Telegram auth")

        return user_data

    def verify_telegram_data(self, init_data: str) -> UserCreateUpdate | None:
        try:
            parsed_data = dict(parse_qsl(init_data))
            hash_str = parsed_data.pop("hash")

            data_check_string = "\n".join(
                f"{key}={value}"
                for key, value in sorted(parsed_data.items(), key=itemgetter(0))
            )

            secret_key = hmac.new(
                key=b"WebAppData",
                msg=settings.tg.token.encode(),
                digestmod=hashlib.sha256,
            )
            computed_hash = hmac.new(
                key=secret_key.digest(),
                msg=data_check_string.encode(),
                digestmod=hashlib.sha256,
            ).hexdigest()

            user_json = parsed_data["user"]  # JSON-строка
            user_dict = orjson.loads(user_json)

            if computed_hash == hash_str:
                return UserCreateUpdate(**user_dict)
        except ValueError:
            return None
