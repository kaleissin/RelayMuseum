#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

README_FILE = open('README.rst')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()

setup(name='RelayMuseum',
        version='0.4.0',
        packages=['relay', 'RelayMuseum'],
        package_dir={'': 'src'},
        include_package_data=True,
        zip_safe=False,
        platforms=['any'],
        description='A web-museum for conlang-relays.',
        author_email='kaleissin@gmail.com',
        author='kaleissin',
        url='https://github.com/kaleissin/RelayMuseum',
        long_description=long_description,
        classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Topic :: Software Development :: Libraries :: Application Frameworks',
                'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
