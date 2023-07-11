from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, status


api_key = '051d8c8f59a23844dfb7979fec4349544829d153b5280bf191376c0f7de0fc9e'
api_key_header = APIKeyHeader(name = 'accessKey', auto_error = False)


async def verify_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != api_key:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Missing or invalid accessKey in request header.'
        )