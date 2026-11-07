import unittest

from guardian.pipeline.guardian_pipeline import GuardianPipeline
from guardian.pipeline.stages import Stage


class TestGuardianPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = GuardianPipeline()

    def test_loop_starts_and_ends_at_root(self):
        ctx = self.pipeline.process("contoh input")
        self.assertEqual(ctx.audit_log[0][0], Stage.ROOT.name)
        self.assertEqual(ctx.audit_log[-1][0], Stage.ROOT.name)

    def test_visits_all_19_stages_plus_root_twice(self):
        ctx = self.pipeline.process("contoh input")
        names = [s for s, _ in ctx.audit_log]
        self.assertEqual(len(names), 21)  # ROOT + 9 luar + 10 dalam + ROOT
        self.assertEqual(names.count(Stage.ROOT.name), 2)

    def test_sanitize_decodes_base64_payload(self):
        import base64
        payload = base64.b64encode(b"hidden instruction").decode()
        ctx = self.pipeline.process(f"prefix {payload}")
        self.assertIn('base64_payload_decoded', ctx.flags['sanitize'])
        self.assertIn("hidden instruction", ctx.text)


if __name__ == '__main__':
    unittest.main()
