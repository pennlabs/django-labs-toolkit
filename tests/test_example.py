from django.test import TestCase

from pennlabs.temp import abc


class ExampleTestCase(TestCase):
    def test_example(self):
        self.assertEqual(abc(), 0)
