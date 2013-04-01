import cPickle as pickle
import urlparse

import requests
from awsauth import S3Auth

import boto
from boto.exception import S3ResponseError
from boto.s3.key import Key


class Client(object):
    def __init__(self, access_key, access_secret, bucket_name):
        self.conn = boto.connect_s3(access_key, access_secret)
        try:
            self.bucket = self.conn.get_bucket(bucket_name)
        except S3ResponseError:
            # If bucket doesn't exist, create it
            # TODO probably set private permissions
            self.bucket = self.conn.create_bucket(bucket_name)
        self.bucket_url = self.conn.calling_format.build_url_base(self.conn, 'http', self.conn.server_name(), self.bucket.name)
        self.session = requests.Session()
        self.session.auth = S3Auth(access_key, access_secret)
    ##### Generic Keys http://redis.io/commands#generic ########################

    def set(self, key_name, value):
        key = Key(self.bucket)
        key.key = key_name
        key.set_contents_from_string(pickle.dumps(value))
        # key.set_acl('public-read')
        return True

    def get(self, key_name):
        key_url = urlparse.urljoin(self.bucket_url, key_name)
        result = self.session.get(key_url)

        if not result.ok:
            return None
        return pickle.loads(result.content)

        # key = self.bucket.get_key(key_name)
        # if key:
        #     return pickle.loads(key.get_contents_as_string())
        # else:
        #     return None

    def delete(self, key_name):
        key = self.get(key_name)
        if key:
            self.bucket.delete_key(key_name)
            return 1
        else:
            return 0

    def keys(self, prefix=None):
        # S3 prefix filtering doesn't need *s
        if prefix:
            prefix = prefix.rstrip("*")

        result = []
        for key in self.bucket.get_all_keys(prefix=prefix):
            result.append(key.key)
        return result

    def exists(self, key_name):
        return bool(self.get(key_name))

    ##### Set Keys http://redis.io/commands#set ################################

    def sadd(self, key_name, value):
        curr_value = self.get(key_name)
        if curr_value:
            if value in curr_value:
                return 0
            else:
                curr_value.add(value)
                self.set(key_name, curr_value)
                return 1
        else:
            self.set(key_name, set([value]))
            return 1

    def smembers(self, key_name):
        return self.get(key_name) or []

    def scard(self, key_name):
        return len(self.smembers(key_name))
