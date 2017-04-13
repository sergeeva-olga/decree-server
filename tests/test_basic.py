from nose.plugins.skip import SkipTest
from nose.tools import assert_raises
from isu.aquarium import russian

#@SkipTest


class TestsBasic:

    def setUp(self):
        pass

    def test_something(self):
        assert 1 + 1 == 2

    def tearDown(self):
        pass

    def test_Russian(self):
        russian.test_names()
