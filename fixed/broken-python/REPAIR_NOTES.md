# Fixed `martinpeck/broken-python` Copy

This folder contains a repaired copy of the upstream `martinpeck/broken-python` examples used in the EX04 investigation.

## Files Recreated

| Upstream file | Fixed file | Main repairs |
|---|---|---|
| `mathsquiz/mathsquiz.py` | `fixed/broken-python/mathsquiz/mathsquiz.py` | Python 3 syntax, correct answers, score increments, 10 questions, valid branching. |
| `mathsquiz/mathsquiz-step1.py` | `fixed/broken-python/mathsquiz/mathsquiz-step1.py` | Keeps checkpoint behavior but removes repetition through shared quiz core. |
| `mathsquiz/mathsquiz-step2.py` | `fixed/broken-python/mathsquiz/mathsquiz-step2.py` | Removes global `score` bug from final score reporting. |
| `mathsquiz/mathsquiz-step3.py` | `fixed/broken-python/mathsquiz/mathsquiz-step3.py` | Removes global `score` bug and keeps random generation testable. |
| `polygons/polygons.py` | `fixed/broken-python/polygons/polygons.py` | Fixes undefined base class, invalid `new`, formula logic, drawing loop, and import-time prompts. |

The shared `mathsquiz/quiz_core.py` module is an added improvement layer used by the fixed quiz scripts.
