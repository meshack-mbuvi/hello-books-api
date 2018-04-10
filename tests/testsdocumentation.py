import unittest
from instance.config import configuration
from application import app


class UserTests(unittest.TestCase):

    def setUp(self):
        """Prepares variables to be used by test methods"""

        # create new user
        self.app = app
        self.app.config.from_object(configuration['testing'])
        self.app = self.app.test_client()
        self.BASE_URL = '/api/v1/auth/'

    def test_can_find_documentation(self):
        response = self.app.get('/api/v1/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
