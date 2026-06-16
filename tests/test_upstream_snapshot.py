import importlib.util
import unittest
from pathlib import Path


class UpstreamSnapshotTests(unittest.TestCase):
    def test_original_bug_is_reproduced(self):
        root = Path(__file__).resolve().parents[1]
        snapshot = root / "data" / "upstream_snapshot" / "scheduler_bug.py"
        spec = importlib.util.spec_from_file_location("scheduler_bug", snapshot)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        text = "deploy | Deploy app | 1 | test\ntest | Run tests | 2 |"
        with self.assertRaises(ValueError) as error:
            module.parse_plan(text)
        self.assertIn("unknown dependency", str(error.exception))


if __name__ == "__main__":
    unittest.main()
