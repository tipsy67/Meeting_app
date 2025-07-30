import asyncio
import datetime
from pathlib import Path

from fluent.runtime import FluentResourceLoader, FluentLocalization

from api_app.core.config import settings
from api_app.schemas.users import UserResponse, UserCreateUpdate


class L10n:
    def __init__(self):
        locales_dir = Path(__file__).parent.parent / "locales"
        self.loader = FluentResourceLoader(str(locales_dir / "{locale}"))
        self.l10n = {
            "en": FluentLocalization(["en"], ["messages.ftl"], self.loader),
            "ru": FluentLocalization(["ru"], ["messages.ftl"], self.loader),
        }
        self.default_locale = settings.default_language_code

    async def translate(self, user: UserResponse, message_id: str, **kwargs) -> str:
        locale = (
            getattr(user, "language_code", self.default_locale).split("-")[0].lower()
        )
        locale = locale if locale in self.l10n else self.default_locale
        return self.l10n[locale].format_value(message_id, kwargs)

    async def format_time(self, user: UserResponse, delta) -> str:
        minutes, seconds = divmod(delta.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days = delta.days

        return await self.translate(
            user,
            "time-duration",
            days=days,
            hours=hours,
            minutes=minutes,
        )


l10n = L10n()


async def main():
    test_user = UserCreateUpdate(**{"id": "2222", "first_name": "test"})
    test_user.language_code = "ru"
    print("Test translation:", await l10n.translate(test_user, "attention-message"))
    params1 = {
        "recipient_name": "Alice",
        "initiator_name": "Bob",
        "initiator_username": None,
        "text": "bnkbnkbn",
    }
    print(await l10n.translate(test_user, "attention-message", **params1))

    delta = datetime.timedelta(days=1, hours=2, minutes=30)
    print("Formatted duration (ru):", await l10n.format_time(test_user, delta))
    test_user.language_code = "en"
    print("Formatted duration (en):", await l10n.format_time(test_user, delta))


if __name__ == "__main__":
    asyncio.run(main())
