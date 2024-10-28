from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner

from seeds_shop.core.models.enums.user import LangCode


class LocaleLoader:
    def __init__(self, locales_folder: Path):
        self.locales_folder = locales_folder

    def get_content(self, locale: str) -> str | None:
        with open(self.locales_folder / f"{locale}.ftl", encoding="utf-8") as f:
            return f.read()


class Locale(FluentTranslator):
    """Facade for l10n, i18n and translation.
    Uses FluentTranslator at backend."""


class Localizator:
    """Pool of Locale objects."""

    def __init__(self, loader, locales_map: dict, default_locale="ru"):
        self.loader = loader
        self._map = locales_map
        self.default_locale = default_locale

        translators = []

        for lang in locales_map:
            trans = FluentTranslator(
                lang,
                translator=FluentBundle.from_string(
                    lang,
                    self.loader.get_content(lang),
                    use_isolating=False,
                ),
            )

            translators.append(trans)

        self.hub = TranslatorHub(
            locales_map,
            translators=translators,
            root_locale=default_locale,
        )

    def get_by_locale(self, locale: str | LangCode) -> TranslatorRunner:
        if isinstance(locale, LangCode):
            locale = locale.value
        if locale not in self._map:
            return self.hub.get_translator_by_locale(self.default_locale)
        return self.hub.get_translator_by_locale(locale)


def configure_localizator(locales_path: str):
    locales_map = {
        "ru": ("ru",),
        "en": ("en",),
    }
    loader = LocaleLoader(
        Path(locales_path),
    )
    return Localizator(loader, locales_map)
