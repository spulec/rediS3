#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='rediS3',
    version='0.0.1',
    description='RediS3 is an implementation of the Redis API using S3 as a backend',
    author='Steve Pulec',
    author_email='spulec@gmail',
    url='https://github.com/spulec/rediS3',
    packages=find_packages(),
    install_requires=[
        "boto",
    ],
)