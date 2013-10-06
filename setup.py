import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.mkd')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'polling',
    version = '0.1',
    packages = find_packages(exclude=['demo', 'demo.*','doc','doc.*']),
    include_package_data = True,
    license = '',
    description = '',
    long_description = '',
    url = '#',
    author = 'firdan, asep',
    author_email = '',
    download_url='',
    install_requires = [
        'django-registration',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: ',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

