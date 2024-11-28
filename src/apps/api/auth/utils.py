import base64
import imghdr
import logging
import os

from fastapi import Depends

from src.apps.api import exceptions
from src.apps.api.auth.crud import get_user_data_obj
from src.apps.api.auth.jwt_conf import JwtBearer
from src.db import db_helper

logger = logging.getLogger(__name__)


async def base64_image_saver(img_folder: str, image_base64: str, uuid: str) -> str:
    from src.fastapi_core import APP_ROOT

    image_data = base64.b64decode(image_base64)

    file_name = f"{uuid}.png"
    file_path = APP_ROOT / f"media/{img_folder}/{file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(image_data)

    image_path = f"media/{img_folder}/{file_name}"
    return image_path


def check_image_type(value: str) -> str:
    image_data = base64.b64decode(value)
    image_type = imghdr.what(None, h=image_data)
    if image_type not in ['jpeg', 'png', 'jpg']:
        raise ValueError("Unsupported image type")
    return image_type


def role_check(allowed_roles: list):

    async def check_role(token_payload: dict = Depends(JwtBearer())):
        async with db_helper.session_factory() as session:
            user_role = (await get_user_data_obj(
                session=session, uuid=token_payload['uuid']
            )).role
        if user_role not in allowed_roles:
            raise exceptions.permission_denied

    return check_role
