import io

from fastapi import APIRouter, Depends
from pydantic import constr
from starlette.responses import StreamingResponse

from core.controller import user
from storage.tortoise import SceneDataSchema, SceneData

router = APIRouter(tags=['Misc'], prefix='/misc')


@router.get('/miniprogram_code', description='Generate a miniprogram code with given data', status_code=201)
async def miniprogram_code_unlimited(image: bytes = Depends(user.create_wxa_code_unlimited)):
    return StreamingResponse(io.BytesIO(image), media_type='image/png')


@router.get('/data_from_key', description="Get data from key", response_model=SceneDataSchema)
async def get_data_from_key(key: constr(min_length=5, max_length=28), ):
    return await SceneDataSchema.from_tortoise_orm(await SceneData.get(key=key))
