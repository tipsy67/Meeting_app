import os.path
from pathlib import Path

from aiogram.utils.i18n import I18n, SimpleI18nMiddleware


BASE_BOT_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = Path(os.path.join(BASE_BOT_DIR, 'locales'))
print(LOCALES_DIR.exists())
for lang_dir in LOCALES_DIR.iterdir():
    if lang_dir.is_dir():
        print(f"  {lang_dir.name}:")
        for file in lang_dir.glob("*.ftl"):
            print(f"    - {file.name}")
i18n = I18n(path=LOCALES_DIR, default_locale='en', domain='messages')
lang_middleware = SimpleI18nMiddleware(i18n)
print(f"Available locales: {i18n.available_locales}")