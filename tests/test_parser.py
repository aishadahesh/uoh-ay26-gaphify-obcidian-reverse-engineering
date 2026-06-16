import unittest

from gaphify_re.parser import ParseError, parse_plan
from gaphify_re.scheduler import CycleError, schedule, topological_order


class ParserTests(unittest.TestCase):
    def test_forward_dependency_is_valid_after_fix(self):
        text = "deploy | Deploy app | 1 | test\ntest | Run tests | 2 |"
        plan = parse_plan(text)
        self.assertEqual([task.task_id for task in topological_order(plan)], ["test", "deploy"])

    def test_missing_dependency_still_fails(self):
        with self.assertRaises(ParseError):
            parse_plan("deploy | Deploy app | 1 | missing")

    def test_schedule_uses_dependency_finish_time(self):
        plan = parse_plan("deploy | Deploy app | 1 | test\ntest | Run tests | 2 |")
        self.assertEqual(schedule(plan), {"test": 2, "deploy": 3})

    def test_cycle_detection(self):
        plan = parse_plan("a | A | 1 | b\nb | B | 1 | a")
        with self.assertRaises(CycleError):
            topological_order(plan)


if __name__ == "__main__":
    unittest.main()
