from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common.when import WhenCondition
from aiogram_dialog.widgets.kbd import SwitchInlineQuery
from aiogram_dialog.widgets.text import Text

from seeds_shop.tg_bot.services.locale import Locale


class LocaleText(Text):
    def __init__(
        self,
        i18n_var_name: str,
        when: WhenCondition = None,
        localizator_name="locale",
        **kwargs,
    ):
        super().__init__(when=when)
        self.v_name = i18n_var_name
        self._kwargs = kwargs
        self._l_name = localizator_name

    async def _render_text(
        self,
        data: dict,
        manager: DialogManager,
    ) -> str:
        mw_d = manager._data
        locale: Locale = mw_d.get(self._l_name)
        data_to_pass = {}

        data_to_pass.update(data)

        for k, v in self._kwargs.items():
            if not isinstance(v, str):
                data_to_pass[k] = v
                continue
            try:
                data_to_pass[k] = v.format_map(data)
            except KeyError:
                data_to_pass[k] = "%nodata%"

        res = locale.get(self.v_name, **data_to_pass)
        if res is None:
            return f"[{self.v_name}]: locale error, check localization files"
        return res


class SwitchInlineQueryCurrentChat(SwitchInlineQuery):
    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    switch_inline_query_current_chat=await self.switch_inline.render_text(
                        data,
                        manager,
                    ),
                ),
            ],
        ]
