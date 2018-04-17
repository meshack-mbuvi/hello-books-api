import unittest

from run import *


class UserTests(unittest.TestCase):

    def setUp(self):
        """Prepares variables to be used by test methods."""
        app.config.from_object(configuration['testing'])
        self.app = app.test_client()

    def test_can_find_documentation(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
