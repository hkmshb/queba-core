# -*- coding: utf-8 -*-
from setuptools import setup
import queba.core


setup(
    name='queba.core',
    version=queba.core.__version__,
    description='QuEBA Core Library',
    long_description=queba.core.__doc__,
    author=queba.core.__author__,
    author_email='hkmshb@gmail.com',
    url='http://hazeltek.com/',
    license='None',
    platforms='any',
    packages=['queba'],    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Libraries ',
    ],
)
