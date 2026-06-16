import unittest

from gaphify_re.token_meter import estimate_tokens


class TokenMeterTests(unittest.TestCase):
    def test_estimate_is_positive(self):
        self.assertGreaterEqual(estimate_tokens("abc"), 1)

    def test_estimate_scales_with_text(self):
        self.assertGreater(estimate_tokens("a" * 80), estimate_tokens("a" * 8))


if __name__ == "__main__":
    unittest.main()
