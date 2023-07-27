from django.core.management.base import BaseCommand
from AppAdmin.models import *
import pika
import time
 
class Command(BaseCommand):
    help = 'Starts consuming messages from RabbitMQ'
    def connect(self):
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
                
    def handle(self, *args, **options): 
        connection = self.connect()
        channel = connection.channel()
        channel.basic_consume(queue='ecoles', on_message_callback=self.get_data_ecole, auto_ack=True)
        channel.basic_consume(queue='directeurs', on_message_callback=self.get_data_directeur, auto_ack=True)
        self.stdout.write(
                self.style.SUCCESS("Started Consuming....")
            )
        channel.start_consuming()
        connection.close()
        
    def get_data_ecole(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip() 
        ecole = dict_data['ecole']
        ecoleSave = Ecole(
            ecole=ecole
        )
        ecoleSave.save()
        print("message received successfully")
        
    def get_data_directeur(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip()
        
        nom = dict_data['nom']
        potsnom = dict_data['potsnom']
        prenom = dict_data['prenom']
        email = dict_data['email']
        ecole = dict_data['ecole']
        password = dict_data['password']
        print("consumer ",password)
        get_ecole = Ecole.objects.get(ecole=ecole)
        user = User.objects.create_user(username=nom, first_name=potsnom, last_name=prenom, email=email, password=password, status='directeur')
        directeur = Directeur(
            userId=user,
            ecoleId=get_ecole
        )
        directeur.save()
        print("message received successfully")