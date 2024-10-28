from flask import Blueprint, send_from_directory

from seeds_shop.admin_panel.app.constants import (
    assets_folder,
    covers_folder,
    images_folder,
    invoices_folder,
    media_path,
)

media_bp = Blueprint("media_bp", __name__, static_folder=media_path)


@media_bp.route("/covers/<path:filename>")
def covers(filename: str):
    return send_from_directory(
        covers_folder,
        filename,
    )


@media_bp.route("/product_images/<path:filename>")
def product_images(filename: str):
    return send_from_directory(
        images_folder,
        filename,
    )


@media_bp.route("/assets/<path:filename>")
def assets(filename: str):
    return send_from_directory(
        assets_folder,
        filename,
    )


@media_bp.route("/invoices/<path:filename>")
def invoices(filename: str):
    return send_from_directory(
        invoices_folder,
        filename,
    )
