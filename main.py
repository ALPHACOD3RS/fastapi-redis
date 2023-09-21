from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
import consumers
from redis_om import get_redis_connection, HashModel
import json

app = FastAPI()


redis = get_redis_connection(
    host="redis-12646.c9.us-east-1-4.ec2.cloud.redislabs.com",
    port="12646",
    password="Z4uvm1wbGZL79T3u4IkaUhD4UXcpEziR",
    decode_responses=True

)


class Delivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = redis


@app.post('/delivery/create')
async def root(req: Request):
    body = await req.json()
    print(body)
    delivery = Delivery(
        budget=body['data']['budget'], notes=body['data']['notes']).save()
    event = Event(
        delivery_id=delivery.pk, type=body['type'], data=json.dumps(
            body['data'])
    ).save()
    state = consumers.create_delivery({}, event)
    return state
