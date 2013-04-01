from moto import mock_s3
import rediS3

import sure  # flake8: noqa


@mock_s3()
def test_get_and_set():
    client = rediS3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')

    client.sadd('myset', 'Hello').should.equal(1)
    client.sadd('myset', 'World').should.equal(1)
    client.sadd('myset', 'World').should.equal(0)
    client.smembers('myset').should.equal(set(['Hello', 'World']))
