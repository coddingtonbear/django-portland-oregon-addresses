import logging
import re

logger = logging.getLogger('portland_addresses.management.commands.load_addresses')

class AddressParserException(Exception):
    pass

class InsufficientInformationException(AddressParserException):
    pass

class AddressParser(object):
    SUFFIX_MAP = {
            "ALY": ['ALLEY', ],
            "AVE": ['AVENUE', ],
            "BLVD": ['BOULEVARD', ],
            "CIR": ['CIRCLE', ],
            "CT": ['COURT', ],
            "DR": ['DRIVE', ],
            "HWY": ['HIGHWAY', ],
            "LN": ['LANE', ],
            "LOOP": [],
            "PKWY": ['PARKWAY', ],
            "PL": ['PLACE', ],
            "RD": ["ROAD", ],
            "ST": ['STREET', ],
            "TER": ['TERRACE', ],
            "WAY": [],
            }

    def __init__(self, string):
        super(AddressParser, self).__init__()
        self.address_string = string

        try:
            self.address_number = None
            self.quadrant = None
            self.street = None
            self.suffix = None
            parts_remaining = self.get_parts(string)
            if parts_remaining:
                self.address_number, parts_remaining = self.get_number(parts_remaining)
            if parts_remaining:
                self.quadrant, parts_remaining = self.get_quadrant(parts_remaining)
            if parts_remaining:
                self.street, self.suffix, parts_remaining = self.get_street_and_suffix(parts_remaining)
            self.extra = parts_remaining
            if not self.street or not self.address_number:
                raise InsufficientInformationException(
                        "Insufficient information provided in address '%s'" % (
                            string
                            )
                        )
        except AddressParserException as e:
            logger.exception(e)
            raise e
        except Exception as e:
            logger.exception(e)
            raise AddressParserException(
                    "Exception encountered while processing address '%s' (%s)" % (
                        string,
                        e
                        )
                    )

        logger.debug(unicode(self))
        if self.extra:
            logger.debug("Found extra parts in address: %s" % self.extra)

    def __str__(self):
        return "%s %s %s %s" % (
            self.address_number,
            self.quadrant if self.quadrant else '',
            self.street,
            self.suffix,
            )

    def __repr__(self):
        return "<ParsedAddress: %s>" % str(self)

    def __unicode__(self):
        return unicode(str(self))

    def __getitem__(self, key):
        if key == 'number':
            return self.address_number
        elif key == 'quadrant':
            return self.quadrant
        elif key == 'street':
            return self.street
        elif key == 'suffix':
            return self.suffix
        elif key == 'extra':
            return self.extra
        else:
            raise IndexError("Key %s does not exist" % key)

    @classmethod
    def get_number(cls, parts):
        logger.debug("Parts: %s" % parts)
        if re.match(r'^\d+$', parts[0]):
            logger.debug("Number: %s" % parts[0])
            number = parts[0]
            parts.remove(parts[0])
            return number, parts
        logger.debug("Number: None")
        return None, parts

    @classmethod
    def get_quadrant(cls, parts):
        logger.debug("Parts: %s" % parts)
        quadrant_raw = parts[0]
        quadrant_raw_extra = parts[1] if len(parts) > 1 else None
        logger.debug("Quadrant Raw: %s (and %s ?)" % (
            quadrant_raw,
            quadrant_raw_extra
            ))
        quadrant = None
        if quadrant_raw in ['NW', 'NORTHWEST', ]:
            parts.remove(quadrant_raw)
            quadrant = 'NW'
        elif quadrant_raw in ['NORTH', 'N', ] and quadrant_raw_extra in ['W', 'WEST']:
            parts.remove(quadrant_raw)
            parts.remove(quadrant_raw_extra)
            quadrant = 'NW'
        elif quadrant_raw in ['NE', 'NORTHEAST', ]:
            parts.remove(quadrant_raw)
            quadrant = 'NE'
        elif quadrant_raw in ['NORTH', 'N', ] and quadrant_raw_extra in ['E', 'EAST']:
            parts.remove(quadrant_raw)
            parts.remove(quadrant_raw_extra)
            quadrant = 'NE'
        elif quadrant_raw in ['SW', 'SOUTHWEST', ]:
            parts.remove(quadrant_raw)
            quadrant = 'SW'
        elif quadrant_raw in ['SOUTH', 'S', ] and quadrant_raw_extra in ['W', 'WEST']:
            parts.remove(quadrant_raw)
            parts.remove(quadrant_raw_extra)
            quadrant = 'SW'
        elif quadrant_raw in ['SE', 'SOUTHEAST', ]:
            parts.remove(quadrant_raw)
            quadrant = 'SE'
        elif quadrant_raw in ['SOUTH', 'S', ] and quadrant_raw_extra in ['E', 'EAST']:
            parts.remove(quadrant_raw)
            parts.remove(quadrant_raw_extra)
            quadrant = 'SE'
        elif quadrant_raw in ['N', 'NORTH']:
            parts.remove(quadrant_raw)
            quadrant = 'N'
        elif quadrant_raw in ['W', 'WEST']:
            parts.remove(quadrant_raw)
            quadrant = 'W'
        elif quadrant_raw in ['E', 'EAST']:
            parts.remove(quadrant_raw)
            quadrant = 'E'
        logger.debug("Quadrant: %s" % quadrant)
        return quadrant, parts

    @classmethod
    def get_street_and_suffix(cls, parts):
        logger.debug("Parts: %s" % parts)
        suffix = ''
        suffix_part = ''
        for part in parts[1:]:
            if suffix:
                break
            for suffix_key, suffix_items in cls.SUFFIX_MAP.items():
                if part == suffix_key or part in suffix_items:
                    suffix_part = part
                    suffix = suffix_key
                    break
        if suffix:
            street_name = " ".join(parts[0:parts.index(suffix_part)])
            final_parts = parts[parts.index(suffix_part) + 1:]
        else:
            street_name = " ".join(parts)
            final_parts = []
        logger.debug("Street: %s %s" % (
            street_name,
            suffix,
            ))
        return street_name, suffix, final_parts

    @classmethod
    def get_parts(cls, address):
        logger.debug("Initial: %s" % address)
        parts_raw = address.split(' ')
        parts = []
        for part in parts_raw:
            cleaned = re.sub(r'[^A-Z0-9-]', '', part.upper()).strip()
            if cleaned:
                parts.append(
                        cleaned
                        )
        return parts
