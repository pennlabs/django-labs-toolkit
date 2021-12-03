from unittest.mock import patch

from django.test import TestCase

from pennlabs.shortener.models import Url


class UrlTestCase(TestCase):
    def setUp(self):
        self.redirect = "https://pennlabs.org"

    def test_exists(self):
        url, created1 = Url.objects.get_or_create(long_url=self.redirect)
        self.assertEqual(Url.objects.all().count(), 1)
        self.assertTrue(created1)
        _, created2 = Url.objects.get_or_create(long_url=self.redirect)
        self.assertFalse(created2)
        self.assertEqual(Url.objects.all().count(), 1)
        self.assertEqual(Url.objects.all()[0], url)

    def test_no_exists(self):
        self.assertFalse(Url.objects.all().exists())
        url, created = Url.objects.get_or_create(long_url=self.redirect)
        self.assertTrue(created)
        self.assertEqual(Url.objects.all().count(), 1)
        self.assertEqual(Url.objects.all().first(), url)

    @patch("pennlabs.shortener.manager.hashlib")
    def test_collision(self, mock_hash):
        mock_hash.sha3_256.return_value.hexdigest.return_value = "abcdef"
        url1, created1 = Url.objects.get_or_create(long_url="url1")
        url2, created2 = Url.objects.get_or_create(long_url="url2")
        self.assertEqual(url1.short_id, "abcde")
        self.assertTrue(created1)
        self.assertEqual(url2.short_id, "abcdef")
        self.assertTrue(created2)
