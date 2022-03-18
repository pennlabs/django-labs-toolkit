from django.shortcuts import reverse
from django.test import TestCase


class EmailPreviewTestCase(TestCase):
    def test_base_view(self):
        response = self.client.get(reverse("email_tools:emailpreview"))
        self.assertTemplateUsed(response, "email_preview.html")

    def test_preview_view(self):
        email = "template"
        variables = {"variable": "{{variable}}"}
        response = self.client.get(reverse("email_tools:emailpreview") + f"?email={email}")
        self.assertEqual(variables, response.context_data["variables"])
        self.assertCountEqual(["complicated", email], response.context_data["templates"])
