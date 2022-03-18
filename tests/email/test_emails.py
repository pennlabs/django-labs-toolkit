from textwrap import dedent

from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase

from pennlabs.emailtools.emails import EmailPreviewContext, html_to_text, send_email
from pennlabs.emailtools.settings import email_settings


class SendEmailTestCase(TestCase):
    def setUp(self):
        self.template = "emails/template.html"
        self.context = {"variable": "value"}
        self.subject = "Subject"
        self.to = "example@example.com"

    def test_defaults(self):
        send_email(self.template, self.context, self.subject, self.to)
        self.assertEqual(1, len(mail.outbox))
        email = mail.outbox[0]
        self.assertEqual(self.subject, email.subject)
        self.assertEqual([self.to], email.to)
        self.assertEqual(email_settings.FROM_EMAIL, email.from_email)
        self.assertIn(self.context["variable"], email.body)

    def test_multiple_to(self):
        self.to = ["example1@example.com", "example2@example.com"]
        send_email(self.template, self.context, self.subject, self.to)
        email = mail.outbox[0]
        self.assertEqual(self.to, email.to)

    def test_sender(self):
        from_email = "new@example.com"
        send_email(self.template, self.context, self.subject, self.to, from_email)
        email = mail.outbox[0]
        self.assertEqual(from_email, email.from_email)

    def test_args(self):
        reply_to = ["reply@example.com"]
        send_email(self.template, self.context, self.subject, self.to, reply_to=reply_to)
        email = mail.outbox[0]
        self.assertEqual(reply_to, email.reply_to)


class HtmlToTextTestCase(TestCase):
    def test_simple(self):
        expected = dedent(
            """
            Very formatted email
            value
            """
        ).strip()
        html = render_to_string("emails/template.html", {"variable": "value"})
        text = html_to_text(html)
        self.assertEqual(expected, text)

    def test_complex(self):
        expected = dedent(
            """
            Important Email
            [fake image]
            - Coffee
            - Tea
            - Milk

            Click the link at https://example.com.
            Example (https://example.com/)


            © 2020 Example
            """
        ).strip()
        html = render_to_string("emails/complicated.html", {"variable": "value"})
        text = html_to_text(html)
        self.assertEqual(expected, text)


class EmailPreviewContextTestCase(TestCase):
    def setUp(self):
        self.key = "key"
        self.value = "value"
        self.pair = {self.key: self.value}
        self.context = EmailPreviewContext(self.pair)

    def test_contains(self):
        self.assertTrue("abc123" in self.context)

    def test_get_item_exists(self):
        self.assertEqual(self.value, self.context[self.key])

    def test_get_item_does_not_exist(self):
        new_key = "key2"
        value = "{{" + new_key + "}}"
        self.assertEqual(value, self.context[new_key])

    def test_get_used_variables(self):
        self.context["key"]
        self.assertEqual(self.pair, self.context.get_used_variables())
