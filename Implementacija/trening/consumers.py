import json
from typing import Any

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from accounts.models import Trening, Korisnik, Rec, Potez


class treningConsumer(WebsocketConsumer):


    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.trening = None
        self.user = None
        self.rec = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['trening_id']
        self.room_group_name = 'trening_%s'%self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        username = text_data_json['username']

        if type == 'initial' and username and self.trening == None:
            trazena = text_data_json['rec']
            self.user = Korisnik.objects.get(username=username)
            self.rec = Rec.objects.get(rec= trazena)
            self.trening = Trening.create_trening(idkor=self.user, rec=self.rec)
            self.trening.save()

            return
        elif type == 'initial' and username =="":
            trazena = text_data_json['rec']
            self.rec = Rec.objects.get(rec=trazena)

        elif type == 'gameterm':
            lives = text_data_json['lives']
            remaining = text_data_json['remaining']

            if self.user:
                if lives == 0:
                   self.trening.idigra.ishod = 1
                if remaining ==0 :
                   self.trening.idigra.ishod = -1

                self.trening.idigra.save()

                self.trening.save()

                self.disconnect(None)



        else:
            message = text_data_json['message']
            succ = text_data_json['succ']
            ishod = (succ=='uspeh')
            lives = text_data_json['lives']

            if self.user:
                potez = Potez(idigra=self.trening.idigra, idkor = self.user, idrec =self.rec, slovo = message, ishod = ishod)
                potez.save()
                print(potez, " saved")







            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'training_message',
                    'message':message,
                    'username':username,
                    'succ':succ,
                    'lives':lives
                }
            )

    def training_message(self,event):
        message =  event['message']
        username = event['username']
        succ = event['succ']
        lives = event['lives']

        self.send(text_data=json.dumps({
            'type':'result_msg',
            'message': message,
            'username': username,
            'succ': succ,
            'lives': lives
        }))