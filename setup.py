#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from djangocms_link_manager import __version__


INSTALL_REQUIRES = [
    'django>=1.8.0',
    'django-cms>=3.0',
    'phonenumberslite>=7.4,<8.0',
    'attrs',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='djangocms-link-manager',
    version=__version__,
    description='An extensible means of checking for broken links in virtually any django CMS plugin.',
    author='Divio',
    author_email='info@divio.com',
    url='https://github.com/divio/djangocms-link-manager/',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    license='LICENSE.txt',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
)
