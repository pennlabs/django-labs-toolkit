from django.test import Client, TestCase
from django.urls import reverse

from pennlabs.options.models import Option


class OptionListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.key = "key"
        self.key2 = "key2"
        self.key3 = "key3"
        self.value = "value"
        self.value2 = "value2"
        self.value3 = "value3"
        self.option = Option.objects.create(
            key=self.key, value=self.value, public=False
        )
        self.option2 = Option.objects.create(
            key=self.key2, value=self.value2, public=True
        )
        self.option3 = Option.objects.create(
            key=self.key3, value=self.value3, public=True
        )

        self.bool_option = Option.objects.create(
            key="boolvalue", value="true", value_type=Option.TYPE_BOOL, public=True
        )
        self.int_option = Option.objects.create(
            key="intvalue", value="3", value_type=Option.TYPE_INT, public=True
        )

    def test_view(self):
        expected = self.option2.serialize()
        expected.update(self.option3.serialize())
        expected.update(self.bool_option.serialize())
        expected.update(self.int_option.serialize())
        response = self.client.get(reverse("options:option-list"))
        self.assertEqual(response.json(), expected)

    def test_view_typed(self):
        resp = self.client.get(reverse("options:option-list"))
        data = resp.json()

        self.assertIsInstance(data["boolvalue"], bool)
        self.assertIsInstance(data["intvalue"], int)
