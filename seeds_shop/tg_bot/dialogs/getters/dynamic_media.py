import contextlib
import os

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from seeds_shop.core.constants import ASSETS_FOLDER


async def phone_asset_getter(dialog_manager: DialogManager, **kwargs):
    phone_hint_video = None
    with contextlib.suppress(TypeError):
        if os.path.isfile(file_path := os.path.join(ASSETS_FOLDER, "phone_hint.mp4")):
            phone_hint_video = MediaAttachment(
                path=file_path,
                type=ContentType.DOCUMENT,
            )

    return {"phone_hint_video": phone_hint_video}


async def name_asset_getter(dialog_manager: DialogManager, **kwargs):
    name_hint_video = None
    with contextlib.suppress(TypeError):
        if os.path.isfile(file_path := os.path.join(ASSETS_FOLDER, "name_hint.mp4")):
            name_hint_video = MediaAttachment(
                path=file_path,
                type=ContentType.DOCUMENT,
            )

    return {"name_hint_video": name_hint_video}
