from fastapi import APIRouter, Depends

from pixoo_app.service.pixoo_interact import get_pixoo_client, PixooService
from super_app.models.yandex_dialogs import AliceRequest, AliceResponse, ResponsePart

router = APIRouter()


@router.post('/pixoo', tags=['alice'], response_model=AliceResponse)
async def alice(
    request: AliceRequest, pixoo_client: PixooService = Depends(get_pixoo_client)
):
    answer = await pixoo_client.get_answer(request.request.nlu.tokens)
    return AliceResponse(
        version=request.version,
        session_id=request.session.session_id,
        response=ResponsePart(text=answer, end_session=True),
    )
