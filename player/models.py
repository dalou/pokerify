# -*- coding: utf8 -*-
from django.db import models as db
from django.contrib.auth.models import User as BaseUser

from poker.room.models import Room
import random, time, types
from datetime import datetime
from poker import player as P, room as R

def request(request, id=None, ask=None):
    pass

class Player(db.Model):    
    name =                  db.CharField(max_length=200, null=False, default="")
    statement =             db.IntegerField(null=False, default=P.S_UP)
    raise_amount =          db.FloatField(null=True, default=None)
    stack =                 db.FloatField(null=False, default=0)
    bet =                   db.FloatField(null=False, default=0)
    room =                  db.ForeignKey(Room, null=False, default=0)
    place =                 db.IntegerField(null=True, default=None)
    cards_in =              db.CharField(max_length=200, default=None, null=True)
    created_at =            db.DateTimeField(default=datetime.now)
    updated_at =            db.DateTimeField(default=datetime.now)
    fake =                  db.BooleanField(default=False)  
   
    def __init__(self, *args, **kwargs):       
        super(Player, self).__init__(*args, **kwargs)
        self.bet = 0 
        self.cards_array = { P.C_CARDS_IN : None }
        if self.cards_in: self.cards_array[P.C_CARDS_IN] = self.cards_in.split(",")      
            
    def save(self, *args, **kwargs):     
        self.cards_in = None       
        if self.cards_array[P.C_CARDS_IN]: self.cards_in = ",".join(self.cards_array[P.C_CARDS_IN])
        self.updated_at = datetime.now()
        super(Player, self).save(*args, **kwargs)       
        
    def prepare(self):
        self.cards(P.C_CARDS_IN, None)  
        if not self.state_is(P.S_UP): 
            self.state(P.S_IDLE)     
        if self.fake:
            self.sitdown()
        if self.state_is(P.S_IDLE):
            return True
        return False
    
    def play(self):
        if self.fake: self.call() 
        if (time.time() - time.mktime(self.updated_at.timetuple())) > P.T_DELAY:
            self.cards(P.C_CARDS_IN, None)
            self.state(P.S_IDLE)    
     
    def state_is(self, *args, **kwargs):
        for arg in args:
            if self.statement == arg: return True
        return False
        
    def state(self, state=None):
        if state != None:
            self.statement = state
            self.save()
            return True
        return self.statement
       
        
    def bet_by(self, amount):
        print amount
        bet = self.stack - amount
        if bet >= 0:
            self.stack = self.stack - bet
            self.bet = self.bet + bet
            return True
        return False
            
    def cards(self, ctype=P.C_CARDS_IN, cards=""):        
        if type(cards) == types.NoneType:            
            if type(ctype) == types.ListType:
                for t in ctype: self.cards_array[t] = None
            else : self.cards_array[ctype] = None
            return None        
        elif type(cards) == types.ListType:
            self.cards_array[ctype] = cards         
        elif type(cards) == types.IntType:  
            if not self.cards_array[ctype]: return None                        
            poped = []
            if cards < 0:
                for i in xrange(abs(cards)):
                    poped.append(self.cards_array[ctype].pop())
            else: poped = self.cards_array[ctype][0:cards:1]
            return poped
        return self.cards_array[ctype]     
    
    def sitdown(self, place=None):
        if self.state_is(P.S_UP):
            self.place = self.room.place_is_free(place)
            print self.place
            if self.place:
                return self.state(P.S_IDLE)
        return False
    
    def situp(self):
        if self.state_is(P.S_WAITING, P.S_IDLE):
            self.place = None
            return self.state(P.S_UP)  
        return False          
    
    def call(self):
        if self.state_is(P.S_WAITING) and self.room.state_is_inturn():
            self.bet_by(self.room.hightbet)
            return self.state(P.S_CALL)
        return False
    
    def raise_by(self, amount):
        player.state = 'RA' 
        self.save()
    
    def fold(self):
        if self.state_is(P.S_WAITING) and self.room.state_is_inturn():
            return self.state(P.S_FOLD)
        return False
    
    def check(self):
        if self.state_is(P.S_WAITING) and self.room.state_is_inturn():
            print self.bet
            print self.room.hightbet
            if self.bet == float(self.room.hightbet):
                return self.state(P.S_CHECK)
        return False
    
    def allin(self):
        if self.state_is(P.S_WAITING) and self.room.state_is_inturn():
            if self.bet(self._stack):
                return self.state(P.S_ALLIN)
        return False
    
    
    
    
        
 