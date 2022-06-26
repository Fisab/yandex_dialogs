from fastapi import APIRouter, Depends

from food_app.service.papa_johns import papa_johns, PapaJohns
from super_app.models.yandex_dialogs import AliceRequest, AliceResponse, ResponsePart
from super_app.models.internal import DeliveryTime, GoodsOutOfStock

router = APIRouter()


@router.get('/goods_out_of_stock', tags=['main'], response_model=GoodsOutOfStock)
async def check_sauce_exists(papa_johns_client: PapaJohns = Depends(papa_johns)):
    result = await papa_johns_client.get_goods_out_of_stock()
    return GoodsOutOfStock(doesnt_exists=result)


@router.get('/delivery_time', tags=['main'], response_model=DeliveryTime)
async def delivery_time(papa_johns_client: PapaJohns = Depends(papa_johns)):
    result = await papa_johns_client.get_delivery_time()
    return DeliveryTime(delivery_time=result)


@router.post('/papa_johns', tags=['alice'], response_model=AliceResponse)
async def alice(
    request: AliceRequest, papa_johns_client: PapaJohns = Depends(papa_johns)
):
    await papa_johns_client.get_goods_out_of_stock()
    answer = await papa_johns_client.get_answer(request.request.nlu.tokens)
    return AliceResponse(
        version=request.version,
        session_id=request.session.session_id,
        response=ResponsePart(text=answer, end_session=True),
    )
