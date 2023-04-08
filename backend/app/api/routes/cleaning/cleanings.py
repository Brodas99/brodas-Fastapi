from typing import List, Union
from fastapi import APIRouter

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK


router = APIRouter()


@router.get("/cleaning/{id}")
async def get_all_cleanings(id: int, name: str = None) -> Union[List[dict], dict]:
    cleanings = [
            {"id": 1, "name": "Bryan", "cleaning_type": "full_clean", "price_per_hour": 29.99},
            {"id": 1, "name": "Axel", "cleaning_type": "full_clean", "price_per_hour": 29.99},
            {"id": 1, "name": "Kelly", "cleaning_type": "full_clean", "price_per_hour": 29.99},
            {"id": 2, "name": "Axel", "cleaning_type": "spot_clean", "price_per_hour": 19.99}
        ]

    if not any(cleaning['id'] == id for cleaning in cleanings):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="This cleaning ID does note exists")
    
    elif not name:
        id_list = []
        for cleaning in cleanings:
            if id == cleaning['id']:
                id_list.append(cleaning)
        return id_list
    
    elif id and name:
        for cleaning in cleanings:
            if name == cleaning['name']:
                return cleaning
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Name does not exists') 