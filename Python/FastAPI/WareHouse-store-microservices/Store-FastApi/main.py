from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.background import BackgroundTasks
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_headers=['*'],
    allow_methods=['*']
)

redis = get_redis_connection(
    host='redis-11158.c212.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=11158,
    password='MDOCEnXB5q8WOoHtK7hzBwvgT9qfQEHP',
    decode_responses=True
)

class ProductOrder(HashModel):
    product_id: str
    quantity: int
    class Meta:
        database = redis
        
class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str
    class Meta:
        database = redis
        
@app.post("/orders")
def create_order(productOrder: ProductOrder, backgroundTask: BackgroundTasks):
    req = requests.get(f"http://localhost:8000/product/{productOrder.product_id}")
    response = req.json()
    fee =  response['price'] * 0.2
    
    order = Order(
        product_id = productOrder.product_id,
        price = response['price'],
        fee = fee,
        total = response['price'] + fee,
        quantity = productOrder.quantity,
        status = 'Pending'    
    )
    order.save()
    
    backgroundTask.add_task(complete_order, order) #Async call where 'complete_order' method is called and 'order' parameter is passed

    return order

@app.get("/orders/{pk}")
def get_order(pk: str):
    return format(pk)

@app.get("/orders")
def get_all_orders():
    return [format(pk) for pk in Order.all_pks()]

def format(pk: str):
    order = Order.get(pk)
    
    return{
        'id': order.pk,
        'product_id': order.product_id,
        'price': order.price,
        'fee': order.fee,
        'total': order.total,
        'quantity': order.quantity,
        'status': order.status
    }
def complete_order(order: Order):
    time.sleep(4)
    order.status = 'completed'
    order.save()
    redis.xadd(name='order-completed', fields=order.dict()) #Redis Stream 