from dishka import Provider, Scope, provide

from seeds_shop.core.constants import LOCALES_FOLDER
from seeds_shop.tg_bot.services.locale import Localizator, configure_localizator


class LocalizatorProvider(Provider):
    scope = Scope.APP

    def __init__(self, locales_path: str = LOCALES_FOLDER):
        super().__init__()
        self.locales_path = locales_path

    @provide
    def get_localizator(self) -> Localizator:
        return configure_localizator(self.locales_path)
