import pickle

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

    ##### Generic Keys http://redis.io/commands#generic ########################

    def set(self, key_name, value):
        key = Key(self.bucket)
        key.key = key_name
        key.set_contents_from_string(pickle.dumps(value))
        return True

    def get(self, key_name):
        key = self.bucket.get_key(key_name)
        if key:
            return pickle.loads(key.get_contents_as_string())
        else:
            return None

    def keys(self, key_name):
        # S3 prefix filtering doesn't need *s
        key_name = key_name.rstrip("*")

        result = []
        for key in self.bucket.get_all_keys(prefix=key_name):
            result.append(pickle.loads(key.get_contents_as_string()))
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
        return self.get(key_name)

    def scard(self, key_name):
        return len(self.smembers(key_name))
