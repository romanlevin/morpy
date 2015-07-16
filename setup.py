# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='morpy',
    version='1.0',
    description='A python tool for finding independent chess positions',
    long_description=readme,
    author='Roman Levin',
    author_email='romanlevin@gmail.com',
    url='https://github.com/romanlevin/morpy',
    packages=['morpy'],
    include_package_data=False,
    entry_points={
        'console_scripts': [
            'morpy=morpy.morpy:main',
        ],
    },
)
