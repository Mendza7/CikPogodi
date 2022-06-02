import json
from time import sleep
from typing import Any

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from accounts.models import Korisnik, Rec, Potez, Partija


class gameConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None
        self.user1 = None
        self.user2 = None
        self.rec1 = None
        self.rec2 = None
        self.lives1 = None
        self.lives2 = None
        self.turn = None
        self.ack = False

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = 'game_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        username = text_data_json['username']

        if type == 'initial' and not self.user1:
            print("Message received" + text_data)
            self.user1 = username
            self.game = Partija.objects.get(idigra_id=int(text_data_json['gameid']))
            u1 = self.game.idkor1
            u2 = self.game.idkor2
            users=[]

            if u1:
                users.append(u1.username)
            if u2:
                users.append(u2.username)

            if username not in users:
                self.close()
            if not self.user2:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'joined',
                        'username': username,
                    }
                )
        elif type == 'moveToServer':
            letter = text_data_json['letter']
            guessing = text_data_json['guessing']
            kor = Korisnik.objects.get(username=username)
            rec = Rec.objects.get(rec=text_data_json['word'])
            success = text_data_json['success'] == True
            remaining = int(text_data_json['rem'])
            potez = Potez(idigra=self.game.idigra, idkor=kor, idrec=rec, slovo=letter, ishod=success)
            potez.save()

            lives = text_data_json['lives']
            if username == self.game.idkor1.username:
                self.game.brojzivota1 = int(lives)
            elif username ==  self.game.idkor2.username:
                self.game.brojzivota2 = int(lives)
            self.game.save()

            if self.game.brojzivota1 == 0:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'gameterm',
                        'winner': self.game.idkor2.username,
                    }
                )
            elif self.game.brojzivota2 == 0:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'gameterm',
                        'winner': self.game.idkor1.username,
                    }
                )
            elif remaining == 0:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'gameterm',
                        'winner': username,
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'moveToClients',
                        'username': username,
                        'guessing': guessing,
                        'lives': lives
                    }
                )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def joined(self, event):
        username = event['username']
        if self.user1 != username:
            if not self.user2:
                self.user2 = username
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'joined',
                        'username': self.user1,
                    }
                )
                print(f"{self.user1} {self.user2}")
                self.send(text_data=json.dumps({
                    'type': 'players',
                    'user1': self.user1,
                    'user2': self.user2
                }))

    def moveToClients(self, event):
        self.send(text_data=json.dumps(event))

    def gameterm(self,event):
        self.send(text_data=json.dumps(event))
