from django.core.management import call_command
from django.test import TestCase
from serializers import UserSerializer, SchoolSerializer

class MixinTestCase(TestCase):
    def setUp(self):
        pass