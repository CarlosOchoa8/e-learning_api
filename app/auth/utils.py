from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials


def get_token_auth_header(credentials: HTTPAuthorizationCredentials) -> str:
    """Obtains the Access Token from the Authorization Header"""
    if not credentials:
        raise HTTPException(
            detail="Authorization header is expected",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            detail="Authorization header must start with Bearer",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return credentials.credentials


def credentials_exception() -> HTTPException:
    """
    Raise an exception if credentials are invalid.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
