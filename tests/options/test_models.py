from django.core.exceptions import ValidationError
from django.test import TestCase

from pennlabs.options.models import (
    Option,
    get_bool,
    get_option,
    get_value,
    is_bool,
    is_int,
)


class OptionTestCase(TestCase):
    def setUp(self):
        self.key = "key"
        self.value = "value"
        self.option = Option.objects.create(key=self.key, value=self.value)

    def test_str(self):
        self.assertEqual(str(self.option), f"{self.key}->{self.value}")

    def test_serialize(self):
        expected = {self.key: self.value}
        self.assertEqual(self.option.serialize(), expected)

    def test_as_int_int(self):
        self.option.value = "123"
        self.option.value_type = Option.TYPE_INT
        self.assertEqual(self.option.as_int(), 123)

    def test_as_int_text(self):
        self.assertIsNone(self.option.as_int())

    def test_as_bool_bool(self):
        self.option.value = "tRuE"
        self.option.value_type = Option.TYPE_BOOL
        self.assertTrue(self.option.as_bool())

    def test_as_bool_text(self):
        self.assertIsNone(self.option.as_bool())

    def test_clean_invalid_int(self):
        self.option.value_type = Option.TYPE_INT
        self.assertRaises(ValidationError, self.option.save)

    def test_clean_invalid_bool(self):
        self.option.value_type = Option.TYPE_BOOL
        self.assertRaises(ValidationError, self.option.save)

    def test_typed_value_setter(self):
        self.key = "key2"
        self.value = "1"
        self.option = Option.objects.create(key=self.key, value=self.value, value_type="Integer")
        self.option.typed_value = 2
        self.assertEquals(self.option.typed_value, "2")


class UtilsTestCase(TestCase):
    def setUp(self):
        self.key = "key"
        self.value = "value"
        self.option = Option.objects.create(key=self.key, value=self.value)

    def test_valid_int(self):
        self.assertTrue(is_int("1"))

    def test_invalid_int(self):
        self.assertFalse(is_int("a"))

    def test_valid_bool(self):
        self.assertTrue(is_bool("true"))

    def test_invalid_bool(self):
        self.assertFalse(is_bool("invalid"))

    def test_get_option_exists(self):
        self.assertEqual(get_option(self.key), self.option)

    def test_get_option_no_exists(self):
        self.assertIsNone(get_option("invalid"))

    def test_get_value_exists(self):
        self.assertEqual(get_value(self.key), self.value)

    def test_get_value_no_exists(self):
        self.assertIsNone(get_value("invalid"))

    def test_get_bool_exists_not_bool(self):
        self.assertIsNone(get_bool(self.key))

    def test_get_bool_exists_is_bool(self):
        self.option.value_type = Option.TYPE_BOOL
        self.option.value = "TruE"
        self.option.save()
        self.assertTrue(get_bool(self.key))

    def test_get_bool_no_exists(self):
        self.assertIsNone(get_bool("invalid"))
