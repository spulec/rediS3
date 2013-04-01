# RediS3

[![Build Status](https://travis-ci.org/spulec/rediS3.png?branch=master)](https://travis-ci.org/spulec/RediS3)
[![Coverage Status](https://coveralls.io/repos/spulec/rediS3/badge.png?branch=master)](https://coveralls.io/r/spulec/RediS3)

# In a nutshell

RediS3 is an implementation of the Redis API using S3 as a backend

# Why

- Memory is expensive, disk is cheap
- S3 is extremely durable
- S3 can be accessed from the client
- S3 scales infinitely

# Basic key get/set

```python

    >>> import redis3
    >>> r = redis3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')
    >>> r.set('foo', 'bar')
    True
    >>> r.get('foo')
    'bar'

```

# Sets

```python

    >>> import redis3
    >>> r = redis3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')
    >>> r.sadd('myset', 'Hello')
    1
    >>> r.sadd('myset', 'World')
    1
    >>> r.sadd('myset', 'World')
    0
    >>> r.smembers('myset')
    ['Hello', 'World']
```

## Install

```console
$ pip install redis3
```
