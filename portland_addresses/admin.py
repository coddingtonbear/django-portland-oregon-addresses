from django.contrib.gis import admin

from portland_addresses.models import Address

class AddressAdmin(admin.options.OSMGeoAdmin):
    search_fields = (
            'address_number',
            'quadrant',
            'street_name',
            'suffix',
            )
    list_display = (
            'address_number',
            'quadrant',
            'street_name',
            'suffix',
            )

admin.site.register(Address, AddressAdmin)
