import io

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from core.controller import user

router = APIRouter(tags=['Misc'], prefix='/misc')


@router.get('/miniprogram_code', description='Generate a miniprogram code with given data', status_code=201)
async def miniprogram_code_unlimited(image: bytes = Depends(user.create_wxa_code_unlimited)):
    return StreamingResponse(io.BytesIO(image), media_type='image/png')
