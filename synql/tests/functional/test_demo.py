from synql.tests import *

class TestDemoController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='demo', action='index'))
        # Test response...
