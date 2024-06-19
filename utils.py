import time
import pika
from consts import *

def connect_to_rmq_server():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f'Błąd połączenia: {e}. Ponowna próba za 2 sekundy.')
            time.sleep(2)