from nose.tools import *
from NAME import myfile


def setup():
    print "SETUP!"


def teardown():
    print "TEARDOWN!"


def test_basic():
    print "I RAN!"
