import pika 
import time

def connect():
    while True:
        try:
            credentials = pika.PlainCredentials('guest', 'guest')
            connection  = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='localhost',
                    port=5672,
                    virtual_host='/',
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)

connection = connect()
channel = connection.channel()
channel.exchange_declare('operations', durable=True, exchange_type='topic')
#===========================Directeur produit pour l'admin==============================================
channel.queue_declare(queue= 'classes')
channel.queue_bind(exchange='operations', queue='classes', routing_key='classes')
channel.queue_declare(queue= 'eleves')
channel.queue_bind(exchange='operations', queue='eleves', routing_key='eleves')
channel.queue_declare(queue= 'elections')
channel.queue_bind(exchange='operations', queue='elections', routing_key='elections')
channel.queue_declare(queue= 'candidats')
channel.queue_bind(exchange='operations', queue='candidats', routing_key='candidats')
#===========================Directeur produit pour l'eleve==============================================
channel.queue_declare(queue= 'eleveclasses')
channel.queue_bind(exchange='operations', queue='eleveclasses', routing_key='eleveclasses')
channel.queue_declare(queue= 'eleveeleves')
channel.queue_bind(exchange='operations', queue='eleveeleves', routing_key='eleveeleves')
channel.queue_declare(queue= 'eleveelections')
channel.queue_bind(exchange='operations', queue='eleveelections', routing_key='eleveelections')
channel.queue_declare(queue= 'elevecandidats')
channel.queue_bind(exchange='operations', queue='elevecandidats', routing_key='elevecandidats')

def publish_message(routing_key, message):
    try:
        channel.basic_publish(
            exchange='operations', 
            routing_key=routing_key, 
            body= message
        )
        print("Message posted successfully")
    except pika.exceptions.AMQPChannelError as e:
        print("Error posting message: ", e)