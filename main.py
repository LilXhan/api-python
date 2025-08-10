from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12701: {
        'weight': 0.5,
        'content': 'glassware',
        'status': 'placed'
    },
    12702: {
        'weight': 2.3,
        'content': 'books',
        'status': 'shipped'
    },
    12703: {
        'weight': 7.8,
        'content': 'electronics',
        'status': 'in transit'
    },
    12704: {
        'weight': 1.2,
        'content': 'clothing',
        'status': 'delivered'
    },
    12705: {
        'weight': 15.0,
        'content': 'furniture',
        'status': 'pending'
    }
}

# http://127.0.0.1:8000/shipment/latest
@app.get('/shipment/latest')
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id] 

# http://127.0.0.1:8000/shipment?id=1421
@app.get('/shipment')
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id doesn\'t exists'
        )
    return shipments[id]

# http://127.0.0.1:8000/shipment?weight=1.8
# BODY -> JSON: { content: 'box' }
@app.post('/shipment')
def submit_shipment(weight: float, data: dict[str, str]) -> dict[str,Any]:
    content = data['content']
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Maximum weight limit is 25kg'
        )

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        'weight': weight,
        'content': content,
        'status': 'placed'
    }

    return {
        'id': new_id
    }

# http://127.0.0.1:8000/shipment/content?id=12704
@app.get('/shipment/{field}')
def get_shipment_fieldd(field: str, id: int) -> Any:
    return shipments[id][field]
   
@app.put('/shipment')
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {
        'content': content, 
        'weight': weight,
        'status': status
    }
    return shipments[id];

@app.patch('/shipment')
def patch_shipment(
    id: int, body: dict[str, Any]
): 
    shipment = shipments[id]
    # Update the provided fields
    # if content:
    #     shipment['content'] = content
    # if weight:
    #     shipment['weight'] = weight
    # if status:
    #     shipment['status'] = status

    shipment.update(body)

    shipments[id] = shipment
    return shipment

@app.delete('/shipment')
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {'detail': f'shipment with id #{id} is deleted!'}
# @app.get('/shipment/{id}')
# def get_shipment(id: int) -> dict[str, Any]:
#     if id not in shipments:
#         return {'details': 'Given id doesn\'t exist!'}
#     return shipments[id]


@app.get('/scalar', include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title='Scalar API'
    )