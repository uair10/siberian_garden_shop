from aiogram_dialog import DialogManager


async def copy_start_data_to_ctx(_, dialog_manager: DialogManager) -> None:
    ctx = dialog_manager.current_context()

    if isinstance(ctx.start_data, dict):
        ctx.dialog_data.update(ctx.start_data)
