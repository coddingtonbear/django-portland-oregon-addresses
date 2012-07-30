from distutils.core import setup

setup(
    name='django-portland-oregon-addresses',
    version='1.0.1',
    url='http://bitbucket.org/latestrevision/django-portland-oregon-addresses/',
    description='Geocode as many addreses in Portland, OR as you would like.',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    packages=[
        'portland_addresses', 
        'portland_addresses.management',
        'portland_addresses.management.commands',
        'portland_addresses.migrations',
        ],
)
