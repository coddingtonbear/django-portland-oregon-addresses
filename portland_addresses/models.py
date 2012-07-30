import logging

from django.contrib.gis.db import models

from portland_addresses.address_parser import AddressParser

logger = logging.getLogger('portland_addresses.models')

class Address(models.Model):
    address_id = models.PositiveIntegerField(
            primary_key=True,
            )
    address_number = models.CharField(
            max_length=6
            )
    quadrant = models.CharField(
            max_length=2,
            choices = (
                ('N', 'N'),
                ('NE', 'NE'),
                ('NW', 'NW'),
                ('SE', 'SE'),
                ('SW', 'SW'),
                ('W', 'W'),
                ('E', 'E'),
                ('', ''),
                )
            )
    street_name = models.CharField(
            max_length="25",
            db_index=True
            )
    suffix = models.CharField(
            max_length="4"
            )
    location = models.PointField(
            srid=2913,
            )
    
    objects = models.GeoManager()

    @classmethod
    def get_by_address(cls, address_string):
        address = AddressParser(address_string)
        try:
            return cls.objects.filter(
                    address_number=address['number'],
                    quadrant=address['quadrant'] if address['quadrant'] else '',
                    street_name=address['street'],
                    suffix=address['suffix'] if address['suffix'] else '',
                    )[0]
        except IndexError:
            raise cls.DoesNotExist("No address found matching %s" % address)

    def __unicode__(self):
        return "%s %s %s %s" % (
                self.address_number,
                self.quadrant,
                self.street_name,
                self.suffix,
                )

    class Meta:
        verbose_name_plural = 'Addresses'
