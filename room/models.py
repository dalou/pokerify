# -*- coding: utf8 -*-
from django.db import models as db
from django.contrib.auth.models import User as BaseUser
from datetime import datetime
import random, time, types
from poker import player as P, room as R
    


class Room(db.Model):       
    created_at =            db.DateTimeField(null=False, default=datetime.now)
    updated_at =            db.DateTimeField(null=False, default=datetime.now)
    place_max =             db.IntegerField(null=False, default=5)
    current_place =         db.IntegerField(null=False, default=2)
    dealer_place =          db.IntegerField(null=True, default=1)
    stack =                 db.FloatField(null=False, default=0)
    blind =                 db.CharField(max_length=200, null=None, default="1,2")
    player_delay =          db.DateTimeField(null=True, default=None)
    cards_in =              db.CharField(max_length=200, null=True, default=None)
    cards_up =              db.CharField(max_length=200, null=True, default=None)
    cards_br =              db.CharField(max_length=200, null=True, default=None)
    statement =             db.IntegerField(null=False, default=R.S_NEW)
    hightbet =              db.FloatField(null=False, default=0)
    pause_time =            db.IntegerField(null=False, default=R.T_NORMAL_PAUSE)
    
    def __init__(self, *args, **kwargs):   
          
        super(Room, self).__init__(*args, **kwargs)  
        self.cards_array = { R.C_CARDS_IN : None, R.C_CARDS_UP : None, R.C_CARDS_BURNED : None }
        if self.cards_in: self.cards_array[R.C_CARDS_IN] = self.cards_in.split(",") 
        if self.cards_up: self.cards_array[R.C_CARDS_UP] = self.cards_up.split(",")
        if self.cards_br: self.cards_array[R.C_CARDS_BURNED] = self.cards_br.split(",")

        self.place_range = xrange(1, self.place_max, 1)  
        self.players = self.player_set.order_by('place')  
        
    def save(self, *args, **kwargs):  
               
        self.cards_in = None
        self.cards_up = None
        self.cards_br = None        
        if self.cards_array[R.C_CARDS_IN]: self.cards_in = ",".join(self.cards_array[R.C_CARDS_IN])
        if self.cards_array[R.C_CARDS_UP]: self.cards_up = ",".join(self.cards_array[R.C_CARDS_UP])
        if self.cards_array[R.C_CARDS_BURNED]: self.cards_br = ",".join(self.cards_array[R.C_CARDS_BURNED])
        self.updated_at = datetime.now()
        super(Room, self).save(*args, **kwargs)  
        
    def state_is_inturn(self):
        return self.state_is(R.S_PREFLOP, R.S_FLOP, R.S_RIVER, R.S_TURN)
        
    def state_is(self, *args, **kwargs):
        for arg in args:
            if self.statement == arg: return True
        return False
        
    def state(self, s=None):
        if s != None: self.statement = s
        return self.statement
        
    
    def place_is_free(self, place=None ):
        if len(self.players) >= self.place_max: return None        
        if place:
            if place < 1 or place > self.place_max: return None
            for player in self.players:
                if place == player.place: return None
            return place
        else:
            for i in self.place_range:
                if self.place_is_free(i): return i;
        return None
        
    def player(self, state=None, add=0, marker=None):        
        self.current_place += add        
        if self.current_place > self.place_max: self.current_place = 1      
        if not marker: marker = self.current_place
        else : 
            if marker == self.current_place: return None       
        for player in self.players:
            if self.current_place == player.place:
                if not state or player.state_is(state):
                    return player
                
        return self.player(state, +1, marker)   
        
    def dealer(self): 
        for player in self.players:
            if self.dealer_place == player.place: return player
        return None       
        
    def cards(self, ctype=R.C_CARDS_IN, cards="", start=0):
        if type(cards) == types.NoneType:            
            if type(ctype) == types.ListType:
                for t in ctype: self.cards_array[t] = None
            else : self.cards_array[ctype] = None
            return None        
        elif type(cards) == types.ListType:   
            if type(self.cards_array[ctype]) == types.ListType:      
                self.cards_array[ctype].extend(cards)      
            else:
                self.cards_array[ctype] = cards
        elif type(cards) == types.IntType:             
            if not self.cards_array[ctype]: return None                        
            poped = []            
            if cards < 0:
                for i in xrange(abs(cards)):
                    poped.append(self.cards_array[ctype].pop())
            else: 
                poped = self.cards_array[ctype][start:cards:1]
            return poped        
        return self.cards_array[ctype]
    
    def cards_shuffle(self):
        random.shuffle(cards)
        random.shuffle(cards)
        random.shuffle(cards)
    
    def refresh_newgame(self):
        player_sit = 0          
        for player in self.players:
            if player.prepare(): player_sit += 1

        if player_sit > 1:
            self.pause(R.T_NORMAL_PAUSE)
            self.cards([R.C_CARDS_IN, R.C_CARDS_UP, R.C_CARDS_BURNED], None)
            self.cards(R.C_CARDS_IN, R.P_CARDS)
            self.state(R.S_SERVING)
            
    def refresh_serving(self):
        player = self.player(P.S_IDLE)                
        if player:           
            player.cards(R.C_CARDS_IN, self.cards(R.C_CARDS_IN, -2)) 
            player.state(P.S_WAITING)                   
        else:
            self.state(R.S_PREFLOP)
    
    def refresh_preflop(self):  
        player = self.player(P.S_WAITING)
        if player:
            self.pause(R.T_NORMAL_PAUSE)
            player.play()                
        else:
            self.pause(R.T_BIG_PAUSE)
            for player in self.players:
                if player.state_is(P.S_FOLD, P.S_CALL, P.S_CHECK, P.S_RAISE, P.S_ALLIN):
                    player.state(P.S_WAITING)
            self.cards(R.C_CARDS_UP, self.cards(R.C_CARDS_IN, -3))
            self.state(R.S_FLOP)
            
    def refresh_flop(self):  
        player = self.player(P.S_WAITING)
        if player:
            self.pause(R.T_NORMAL_PAUSE)
            player.play()                
        else:
            self.pause(R.T_BIG_PAUSE)
            for player in self.players:
                if player.state_is(P.S_FOLD, P.S_CALL, P.S_CHECK, P.S_RAISE, P.S_ALLIN):
                    player.state(P.S_WAITING)
            self.cards(R.C_CARDS_UP, self.cards(R.C_CARDS_IN, -1))
            self.state(R.S_RIVER)
            
    def refresh_river(self):  
        player = self.player(P.S_WAITING)
        if player:
            self.pause(R.T_NORMAL_PAUSE)
            player.play()           
        else:
            self.pause(R.T_BIG_PAUSE)
            for player in self.players:
                if player.state_is(P.S_FOLD, P.S_CALL, P.S_CHECK, P.S_RAISE, P.S_ALLIN):
                    player.state(P.S_WAITING)
            self.cards(R.C_CARDS_UP, self.cards(R.C_CARDS_IN, -1))
            self.state(R.S_TURN)
            
    def refresh_turn(self):  
        player = self.player(P.S_WAITING)
        if player:
            self.pause(R.T_NORMAL_PAUSE)
            player.play()            
        else:
            self.pause(R.T_BIG_PAUSE)
            for player in self.players:
                if player.state_is(P.S_FOLD, P.S_CALL, P.S_CHECK, P.S_RAISE, P.S_ALLIN):
                    player.state(P.S_WAITING)
            self.state(R.S_NEW)
    
    def pause(self, time=R.T_NORMAL_PAUSE):
        self.pause_time = time      
    
    def refresh(self, force=False):
        if force or (time.time() - time.mktime(self.updated_at.timetuple()) > self.pause_time):
 
            if self.state_is(R.S_NEW): self.refresh_newgame()                    
            elif self.state_is(R.S_SERVING): self.refresh_serving() 
            elif self.state_is(R.S_PREFLOP): self.refresh_preflop()
            elif self.state_is(R.S_FLOP): self.refresh_flop()  
            elif self.state_is(R.S_RIVER): self.refresh_river()  
            elif self.state_is(R.S_TURN): self.refresh_turn()
            elif self.state_is(R.S_END): self.refresh_endgame() 
            self.save()       

          
 