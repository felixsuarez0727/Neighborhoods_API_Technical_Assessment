from fastapi import Response, APIRouter

import json
from utils.constants import ST_START_NUMBER

from utils.geocode import skip_street

router = APIRouter(
    prefix="",
    tags=["Version 1 Routes"],
    responses={404: {"description": "Not found"}},
)


@router.get('/process_adress')
async def process_adress():

    response = skip_street(ST_START_NUMBER)

    return Response(json.dumps(response),media_type='application/json')
