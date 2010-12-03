# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Room'
        db.create_table('room_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('_updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('_place_max', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('_current_place', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('_dealer_place', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('_stack', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('_blind', self.gf('django.db.models.fields.CharField')(default='1,2', max_length=200, null=None)),
            ('_player_delay', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('_cards', self.gf('django.db.models.fields.CharField')(default='1c,2c,3c,4c,5c,6c,7c,8c,9c,10c,11c,12c,13c,1s,2s,3s,4s,5s,6s,7s,8s,9s,10s,11s,12s,13s,1h,2h,3h,4h,5h,6h,7h,8h,9h,10h,11h,12h,13h,1d,2d,3d,4d,5d,6d,7d,8d,9d,10d,11d,12d,13d', max_length=200)),
            ('_flop', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('_turn', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('_river', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('_state', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('_hightbet', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('room', ['Room'])


    def backwards(self, orm):
        
        # Deleting model 'Room'
        db.delete_table('room_room')


    models = {
        'room.room': {
            'Meta': {'object_name': 'Room'},
            '_blind': ('django.db.models.fields.CharField', [], {'default': "'1,2'", 'max_length': '200', 'null': 'None'}),
            '_cards': ('django.db.models.fields.CharField', [], {'default': "'1c,2c,3c,4c,5c,6c,7c,8c,9c,10c,11c,12c,13c,1s,2s,3s,4s,5s,6s,7s,8s,9s,10s,11s,12s,13s,1h,2h,3h,4h,5h,6h,7h,8h,9h,10h,11h,12h,13h,1d,2d,3d,4d,5d,6d,7d,8d,9d,10d,11d,12d,13d'", 'max_length': '200'}),
            '_created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            '_current_place': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            '_dealer_place': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            '_flop': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            '_hightbet': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            '_place_max': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            '_player_delay': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            '_river': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            '_stack': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            '_state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            '_turn': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            '_updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['room']
