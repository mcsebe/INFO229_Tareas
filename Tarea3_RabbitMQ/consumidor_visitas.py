import pika
import pageviewapi 

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#El consumidor utiliza el exchange 'log'
channel.exchange_declare(exchange='logs', exchange_type='fanout')

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    info = body.decode('UTF-8')
    info = info[16:len(info)-1]
    print("Número de visitas en la pagina desde 01/01/2000 hasta 01/01/2021: ", end="")
    vistas = pageviewapi.per_article('en.wikipedia', info, '20000101', '20210101', access='all-access', agent='all-agents', granularity='daily')
    numero = 0
    for i in vistas["items"]:
        numero += i["views"]
    print(numero)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()