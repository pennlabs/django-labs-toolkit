from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from pennlabs.options.models import Option


class SetOptionTestCase(TestCase):
    def setUp(self):
        self.key = "key"
        self.value = "value"
        self.option = Option.objects.create(key=self.key, value=self.value)
        self.out = StringIO()

    def test_create_type(self):
        key = "new_key"
        call_command("setoption", key, "true", "--type=BOOL", stdout=self.out)
        option = Option.objects.get(key=key)
        self.assertIn("Created", self.out.getvalue())
        self.assertIn(str(option), self.out.getvalue())
        self.assertIn(option.value_type, self.out.getvalue())

    def test_create_no_type(self):
        key = "new_key"
        call_command("setoption", key, "new_value", stdout=self.out)
        option = Option.objects.get(key=key)
        self.assertIn("Created", self.out.getvalue())
        self.assertIn(str(option), self.out.getvalue())
        self.assertIn(option.value_type, self.out.getvalue())

    def test_update_type(self):
        call_command("setoption", self.key, "true", "--type=BOOL", stdout=self.out)
        option = Option.objects.get(key=self.key)
        self.assertIn("Updated", self.out.getvalue())
        self.assertIn(str(option), self.out.getvalue())
        self.assertIn(option.value_type, self.out.getvalue())

    def test_update_no_type(self):
        call_command("setoption", self.key, "new_value", stdout=self.out)
        option = Option.objects.get(key=self.key)
        self.assertIn("Updated", self.out.getvalue())
        self.assertIn(str(option), self.out.getvalue())
        self.assertIn(option.value_type, self.out.getvalue())
