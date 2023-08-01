from django.core.management.base import BaseCommand
from AppAdmin.models import *
from AppDirecteur.models import *
from AppEleve.models import *
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
        channel.basic_consume(queue='classes', on_message_callback=self.get_data_classe, auto_ack=True)
        channel.basic_consume(queue='eleves', on_message_callback=self.get_data_eleve, auto_ack=True)
        channel.basic_consume(queue='elections', on_message_callback=self.get_data_election, auto_ack=True)
        channel.basic_consume(queue='candidats', on_message_callback=self.get_data_candidat, auto_ack=True)
        channel.basic_consume(queue='electeurs', on_message_callback=self.get_data_electeur, auto_ack=True)
        
        self.stdout.write(
                self.style.SUCCESS("Started Consuming....")
            )
        channel.start_consuming()
        connection.close()
        
    def get_data_classe(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip() 
        
        classe = dict_data['classe']
        ecole = dict_data['ecole']
        ecoleId = Ecole.objects.get(ecole=ecole)
        saveclasse = Classe(
            classe = classe,
            ecoleId = ecoleId
        )
        saveclasse.save()
        print("message received successfully")
        
    def get_data_eleve(ch, method, properties, body, b):
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
        classe = dict_data['classe']
        password = dict_data['password']
        print("consumer ",password)
        get_classe = Classe.objects.get(classe=classe)
        print(get_classe)
        user = User.objects.create_user(username=nom, first_name=potsnom, last_name=prenom, email=email, password=password, status='eleve')
        eleve = Eleve(
            userId=user,
            classeId=get_classe
        )
        eleve.save()
        print("message received successfully")
        
    def get_data_election(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip() 
            
        ecole = dict_data['ecole']
        debut = dict_data['debut']
        fin = dict_data['fin']
        ecoleId = Ecole.objects.get(ecole=ecole)
        saveElection = Election(
            ecoleId = ecoleId,
            dateDebut = debut,
            dateFin = fin
            
        )
        saveElection.save()
        print("message received successfully")
        
    def get_data_candidat(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip() 
                
        election = dict_data['election']
        electionId = Election.objects.get(ecoleId__ecole=election)
        eleve = dict_data['eleve']
        eleveId = Eleve.objects.get(userId__username=eleve)
        print ("eleveId: ",eleveId," electionId: ",electionId)
        savecandidat = Candidat(
            electionId=electionId,
            eleveId=eleveId
        )
        savecandidat.save()
        print("message received successfully")
        
    def get_data_electeur(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip() 
            
        eleve = dict_data['eleve']
        eleveId = Eleve.objects.get(userId__username=eleve)
        election = dict_data['election']
        electionId = Election.objects.get(ecoleId__ecole=election)
        candidat = dict_data['candidat']
        candidatId = Candidat.objects.get(eleveId__userId__username=candidat)
        print ("eleveId: ",eleveId," electionId: ",electionId," candidatId ", candidatId)
        
        savecandidat = Electeur(
            eleveId=eleveId,
            electionId=electionId,
            candidatId=candidatId
        )
        savecandidat.save()
        print("message received successfully")
