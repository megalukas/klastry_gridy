import time
import pika
import numpy as np
from utils import connect_to_rmq_server
from consts import *


def on_response(ch, method, properties, body):
    response = body.decode()
    print(f'Otrzymano odpowiedź: {response}')

def producer():
    with connect_to_rmq_server() as connection:
        channel = connection.channel()

        channel.queue_declare(queue=TASK_QUEUE)
        channel.queue_declare(queue=RESULT_QUEUE)

        channel.basic_consume(queue=RESULT_QUEUE, on_message_callback=on_response, auto_ack=True)

        large_data_set = np.random.rand(1000000)

        chunk_size = 10000
        for i in range(0, len(large_data_set), chunk_size):
            chunk = large_data_set[i:i+chunk_size]
            message = np.array2string(chunk, separator=',')
            channel.basic_publish(exchange='', routing_key=TASK_QUEUE, body=message)
            print(f'Wysłano fragment danych od {i} do {i+chunk_size}')

        print('Oczekiwanie na odpowiedzi od konsumentów...')
        channel.start_consuming()


if __name__ == '__main__':
    producer()
