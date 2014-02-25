Django-portland-oregon-addresses
================================

Do you need to geocode more addresses in Portland, OR than the Google Maps API will allow? This app will download and import a list of addresses provided by the City of Portland, Oregon, and provide you with an easy method for geocoding addresses you provide

The data that this application downloads and installs [point data provided by the City of Portland, OR](http://www.civicapps.org/datasets/address-points).

Installation
------------

You can either install from pip:

    pip install django-portland-oregon-addresses

*or* checkout and install the source from the [github repository](https://github.com/coddingtonbear/django-portland-oregon-addresses):

    git clone https://github.com/coddingtonbear/django-portland-oregon-addresses.git
    cd django-portland-oregon-addresses
    python setup.py install

Then, import the addresses:

    python manage.py load_addresses

Use
---

Given a string looking anything like one of the below (it is really quite flexible):

* 3800 NW Haight Avenue
* 3800 NORTH WEST Haight Avenue, Portland, OR, 97227, USA
* 3800 NORTHWEST Haight Ave, PDX

You can run code like the following to get the address's location:

    from portland_addresses.models import Address
    from portland_addresses.address_parser import AddressParserException

    try:
        address = Address.get_by_address("3828 N Haight Avenue")
        print address.location  # This is the point corresponding with the above address
    except Address.DoesNotExist:
        print "I couldn't find an address matching this :-\"
    except AddressParserException:
        print "I couldn't parse the address you entered :-("

Commands
--------

`load_addresses`: Download and import addresses provided by the City of Portland, Oregon.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/coddingtonbear/django-portland-oregon-addresses/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
