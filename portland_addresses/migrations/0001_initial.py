# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table('portland_addresses_address', (
            ('address_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('address_number', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('quadrant', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length='25', db_index=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length='4')),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=2913)),
        ))
        db.send_create_signal('portland_addresses', ['Address'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table('portland_addresses_address')


    models = {
        'portland_addresses.address': {
            'Meta': {'object_name': 'Address'},
            'address_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '2913'}),
            'quadrant': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': "'25'", 'db_index': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': "'4'"})
        }
    }

    complete_apps = ['portland_addresses']