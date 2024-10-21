from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

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

class Product(HashModel):
    name: str
    price: float
    quantity: int
    class Meta:
        database= redis 
        
@app.post('/product')
def add_product(product: Product):
    return product.save()

@app.get('/product/{pk}')
def get_product(pk: str):
    return Product.get(pk)

@app.get('/products')
def get_all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    
    return{
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }
    
@app.delete('/delete/{pk}')
def delete_product(pk: str):
    return Product.delete(pk )