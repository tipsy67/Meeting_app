import os.path
from pathlib import Path
from typing import Callable

from aiogram import BaseMiddleware
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from fluent.runtime.fallback import FluentResourceLoader, FluentLocalization


class FluentL10nMiddleware(BaseMiddleware):
    def __init__(self, locales_dir):
        self.loader = FluentResourceLoader(f"{locales_dir}/{{locale}}")
        self.l10ns = {
            'en': FluentLocalization(['en'], ['messages.ftl'], self.loader),
            'ru': FluentLocalization(['ru'], ['messages.ftl'], self.loader),
        }
        self.default_locale = 'en'
        self.supported_locales = set(self.l10ns.keys())

    async def __call__(self, handler, event, data):
        user_locale = self.default_locale
        if hasattr(event.message, 'from_user') and event.message.from_user:
            if event.message.from_user.language_code:
                user_locale = event.message.from_user.language_code.split('-')[0].lower()

        if user_locale not in self.supported_locales:
            user_locale = self.default_locale

        data["l10n"] = self.l10ns[user_locale]
        return await handler(event, data)

# Стандартные функции требуют бинарные файлы mo
# BASE_BOT_DIR = Path(__file__).resolve().parent.parent
# LOCALES_DIR = Path(os.path.join(BASE_BOT_DIR, 'locales'))
# print(LOCALES_DIR.exists())
# for lang_dir in LOCALES_DIR.iterdir():
#     if lang_dir.is_dir():
#         print(f"  {lang_dir.name}:")
#         for file in lang_dir.glob("*.ftl"):
#             print(f"    - {file.name}")
# i18n = I18n(path=LOCALES_DIR, default_locale='en', domain='messages')
# lang_middleware = SimpleI18nMiddleware(i18n)
# print(f"Available locales: {i18n.available_locales}")