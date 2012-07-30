from csv import DictReader
import logging
from optparse import make_option
import os
import shutil
import tempfile
import time
import urllib2
import zipfile

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from portland_addresses.models import Address

logger = logging.getLogger('portland_addresses.management.commands.load_addresses')
logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    URL = "ftp://ftp02.portlandoregon.gov/CivicApps/address.zip"

    option_list = BaseCommand.option_list + (
        make_option('--path',
            dest='path',
            default=None,
            help='Path to CSV'),
        )

    def handle(self, *args, **options):
        if options['path']:
            document = self.get_csv_document_from_path(options['path'])
        else:
            document = self.get_csv_document_from_url(self.URL)
        row_number = 0
        start = time.time()
        for row in document:
            row_number = row_number + 1
            if not row['X'] or not row['Y'] or row['city'] != 'PORTLAND':
                continue
            logger.info("Importing %s %s %s %s (row %s, %s rows/sec)" % (
                row['address_number_char'],
                row['str_predir_code'],
                row['street_name'],
                row['street_type_code'],
                row_number,
                row_number / float(time.time() - start)
                ))
            try:
                address = Address.objects.get(
                        address_id=row['address_id']
                        )
            except Address.DoesNotExist:
                address = Address()
                address.address_id = row['address_id']
                address.address_number = row['address_number_char']
                address.quadrant = row['str_predir_code']
                address.street_name = row['street_name']
                address.suffix = row['street_type_code']
                address.location = Point(float(row['X']), float(row['Y']))
                address.save()
        self.cleanup()

    def load_from_path(self, path):
        reader = DictReader(open(path, 'rb'))
        for row in reader:
            pass

    def cleanup(self):
        shutil.rmtree(self.temporary_directory)

    def _get_csv_path_from_directory(self, directory):
        shapefile_path = None
        for path in os.listdir(directory):
            basename, extension = os.path.splitext(path)
            if extension == '.csv':
                shapefile_path = os.path.join(
                        directory,
                        path
                        )

        return shapefile_path

    def get_csv_document_from_path(self, path):
        logger.info("Opening %s" % path)
        return self._get_csv_document(open(path, 'rb'))

    def get_csv_document_from_url(self, url):
        logger.info("Downloading %s" % url)
        return self._get_csv_document(urllib2.urlopen(url))

    def _get_csv_document(self, filelike):
        self.temporary_directory = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile() as output:
            byte_string = filelike.read(1024**2)
            while byte_string != "":
                output.write(byte_string)
                byte_string = filelike.read(1024**2)
            logger.info("Extracting zip file")
            archive = zipfile.ZipFile(output, 'r')
            archive.extractall(self.temporary_directory)
        logger.info("Finding CSV document")
        csv_path = self._get_csv_path_from_directory(
                self.temporary_directory
                )
        logger.info("Opening CSV document")
        document = DictReader(open(csv_path, 'rb'))
        return document
