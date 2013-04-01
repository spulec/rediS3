from moto import mock_s3
import rediS3

import sure  # flake8: noqa


@mock_s3()
def test_get_and_set():
    client = rediS3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')
    client.set('foo', 'bar').should.equal(True)
    client.get('foo').should.equal('bar')


@mock_s3()
def test_get_keys():
    client = rediS3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')

    client.set('foo', 'bar1')
    client.set('foobar', 'bar2')

    client.set('baz', 'bar3')
    client.set('other', 'bar4')

    client.keys("fo*").should.equal(["foo", "foobar"])

    client.keys("ba*").should.equal(["baz"])

    client.keys("other").should.equal(["other"])


@mock_s3()
def test_exists():
    client = rediS3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')

    client.set('foo', 'bar')

    client.exists("foo").should.equal(True)
    client.exists("foobar").should.equal(False)


@mock_s3()
def test_del():
    client = rediS3.Client(access_key='1234', access_secret='secret', bucket_name='my-bucket')

    client.delete('foo').should.equal(0)

    client.set('foo', 'bar')

    client.delete('foo').should.equal(1)
