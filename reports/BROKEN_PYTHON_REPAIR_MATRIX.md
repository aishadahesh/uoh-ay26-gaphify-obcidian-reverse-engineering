# Broken Python Repair Matrix

This report maps the real `martinpeck/broken-python` files to the fixed copy in this submission.

## Selected Upstream Repository

Repository: `martinpeck/broken-python`

Local upstream copy: `data/upstream_broken_python/`

Fixed copy: `fixed/broken-python/`

## File-by-File Repairs

| Upstream file | Broken behavior found | Fixed file | Verification |
|---|---|---|---|
| `mathsquiz/mathsquiz.py` | Does not compile in Python 3 because of Python 2 `print`, assignment in `if`, and invalid `else if`. It also has wrong answers, repeated labels, no score increments, and fewer than 10 completed questions. | `fixed/broken-python/mathsquiz/mathsquiz.py` plus `quiz_core.py` | `test_upstream_mathsquiz_has_syntax_error`, `test_fixed_mathsquiz_scores_all_correct_answers` |
| `mathsquiz/mathsquiz-step1.py` | Mostly repaired checkpoint, but still highly repetitive and not structured for reuse. | `fixed/broken-python/mathsquiz/mathsquiz-step1.py` plus `quiz_core.py` | Covered through shared quiz-core scoring tests |
| `mathsquiz/mathsquiz-step2.py` | `print_final_scores(final_score)` ignores `final_score` and reads global `score`. | `fixed/broken-python/mathsquiz/mathsquiz-step2.py` plus `quiz_core.py` | `test_upstream_step2_final_scores_uses_global_score_bug`, `test_fixed_step2_final_scores_uses_parameter` |
| `mathsquiz/mathsquiz-step3.py` | `print_final_scores(final_score, max_possible_score)` ignores `final_score` and reads global `score`; random behavior is harder to test directly. | `fixed/broken-python/mathsquiz/mathsquiz-step3.py` plus `quiz_core.py` | `test_upstream_step3_final_scores_uses_global_score_bug`, `test_fixed_step3_random_questions_are_testable` |
| `polygons/polygons.py` | Does not compile because of `new Polygon(...)`; also inherits from undefined `Object`, has hard-coded polygon math, always draws six sides, and prompts at import time. | `fixed/broken-python/polygons/polygons.py` | `test_upstream_polygons_has_syntax_error`, `test_fixed_polygons_calculates_general_formula`, `test_fixed_polygons_rejects_invalid_side_count` |

## Engineering Improvements

The repaired copy does more than patch syntax:

- Moves reusable quiz behavior into `quiz_core.py`.
- Adds function parameters for input/output so tests can run without manual typing.
- Removes global score coupling.
- Adds deterministic final-score classification.
- Uses the general polygon formula `(sides - 2) * 180`.
- Adds validation for invalid polygons.
- Guards interactive scripts with `if __name__ == "__main__"`.
