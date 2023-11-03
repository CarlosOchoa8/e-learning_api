from app import schemas
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def fake_decode_token(token):
    return schemas.UserAuth(
        first_name=token+'Carlos',
        last_name=token+'Ochoa',
        email=token+'ochoa.carlos8@outlok.com'
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    auth_user = fake_decode_token(token)
    return auth_user

