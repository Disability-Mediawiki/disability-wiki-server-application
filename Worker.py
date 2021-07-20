import pika
import time
import fitz
import os


# doc = fitz.open(os.path.dirname(os.path.abspath(__file__)) +'/resources/uploads/CRPD.pdf')

sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
# time.sleep(10)

print(' [*] Connecting to server ...')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    time.sleep(10)
    cmd = body.decode()
# doc = fitz.open(os.path.dirname(os.path.abspath(__file__)) +'/resources/uploads/CRPD.pdf')
    if cmd == 'hey':
        print("hey there")
    elif cmd == 'hello':
        print("well hello there")
    else:
        print("sorry i did not understand ", body)

    print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
