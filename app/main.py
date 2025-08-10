from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import ShipmentRead, ShipmentUpdate, ShipmentCreate

app = FastAPI()

shipments = {
    12701: {
        'weight': 9.5,
        'content': 'glassware',
        'status': 'placed',
        'destination': 11004
    },
    12702: {
        'weight': 2.3,
        'content': 'books',
        'status': 'shipped',
        'destination': 11005
    },
    12703: {
        'weight': 7.8,
        'content': 'electronics',
        'status': 'in transit',
        'destination': 11006
    },
    12704: {
        'weight': 1.2,
        'content': 'clothing',
        'status': 'delivered',
        'destination': 11007
    },
    12705: {
        'weight': 15.0,
        'content': 'furniture',
        'status': 'pending',
        'destination': 11008
    }
}


# http://127.0.0.1:8000/shipment?id=1421
@app.get('/shipment', response_model=ShipmentRead)
def get_shipment(id: int):
    if id not in shipments:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id doesn\'t exists'
        )
    return shipments[id]
   
# http://127.0.0.1:8000/shipment?weight=1.8
# BODY -> JSON: { content: 'box' }
@app.post('/shipment', response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        **shipment.model_dump(),
        'status': 'placed'
    }

    return {
        'id': new_id
    }
   

@app.patch('/shipment', response_model=ShipmentRead)
def patch_shipment(
    id: int, body: ShipmentUpdate
): 
    shipment = shipments[id]
    shipment.update(body.model_dump(exclude_none=True))
    return shipments[id]

@app.delete('/shipment')
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {'detail': f'shipment with id #{id} is deleted!'}


@app.get('/scalar', include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title='Scalar API'
    )