#!/usr/bin/env python

import datetime
import random
import string

import redis
import rediS3

import config


def random_string(length=10):
    return "".join([random.choice(string.lowercase) for x in range(length)])


def test_client(client_name, client):
    set_name = random_string()
    sadd_start = datetime.datetime.now()
    for i in range(10):
        _ = client.sadd(set_name, random_string())
    sadd_end = datetime.datetime.now()

    smembers_start = datetime.datetime.now()
    for i in range(100):
        length = len(client.smembers(set_name))
    smembers_end = datetime.datetime.now()

    set_keys = []
    set_start = datetime.datetime.now()
    for i in range(100):
        key_name = random_string()
        client.set(key_name, random_string())
        set_keys.append(key_name)
    set_end = datetime.datetime.now()

    get_start = datetime.datetime.now()
    for key in set_keys:
        client.get(key)
    get_end = datetime.datetime.now()


    for key in client.keys():
        client.delete(key)

    print "------------{}-----------------".format(client_name)
    print "Set add", (sadd_end - sadd_start).total_seconds()
    print "Set smembers length", (smembers_end - smembers_start).total_seconds()
    print "Key set", (set_end - set_start).total_seconds()
    print "Key get", (get_end - get_start).total_seconds()


def main():
    client = rediS3.Client(access_key=config.AWS_ACCESS_KEY, access_secret=config.AWS_SECRET_KEY, bucket_name=config.AWS_BUCKET)
    test_client("rediS3", client)
    client = redis.from_url(config.REDIS_URL)
    test_client("redis", client)


if __name__ == '__main__':
    main()
