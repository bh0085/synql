from synql.tests import *

class TestGoodmorningController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='goodmorning', action='index'))
        # Test response...
