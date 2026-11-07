import base64
import unittest

from guardian.pipeline.sanitize import sanitize_text


class TestSanitize(unittest.TestCase):
    def test_clean_text_unchanged(self):
        text, flags = sanitize_text("contoh input")
        self.assertEqual(text, "contoh input")
        self.assertEqual(flags, [])

    def test_zero_width_chars_removed(self):
        text, flags = sanitize_text("ignore​this")
        self.assertEqual(text, "ignorethis")
        self.assertIn('zero_width_chars_removed', flags)

    def test_homoglyphs_normalized(self):
        # Cyrillic 'а', 'о', 'е' look like Latin a/o/e
        text, flags = sanitize_text("ignоre")
        self.assertEqual(text, "ignore")
        self.assertIn('homoglyphs_normalized', flags)

    def test_base64_payload_decoded(self):
        payload = base64.b64encode(b"hidden instruction").decode()
        text, flags = sanitize_text(f"prefix {payload}")
        self.assertIn('base64_payload_decoded', flags)
        self.assertIn("hidden instruction", text)


if __name__ == '__main__':
    unittest.main()
