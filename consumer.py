import time
import pika
import pika.exceptions
import numpy as np
from utils import connect_to_rmq_server
from consts import *


def on_request(ch, method, properties, body):
    message = body.decode()
    chunk = np.fromstring(message.strip('[]'), sep=',')
    
    chunk_sum = np.sum(chunk)
    response = f'Suma fragmentu: {chunk_sum}'

    ch.basic_publish(exchange='', routing_key=RESULT_QUEUE, body=response)
    print(f'Przetworzono i wysłano odpowiedź: {response}')

    ch.basic_ack(delivery_tag=method.delivery_tag)

def consumer():
    with connect_to_rmq_server() as connection:
        channel = connection.channel()

        channel.queue_declare(queue=TASK_QUEUE)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=TASK_QUEUE, on_message_callback=on_request)

        print('Oczekiwanie na zadania. Aby zakończyć, naciśnij CTRL+C')
        channel.start_consuming()


if __name__ == '__main__':
    consumer()
