# Hot Context: `martinpeck/broken-python` Repair

## Critical Path

`data/upstream_broken_python/` -> `fixed/broken-python/` -> `tests/test_broken_python_fixed.py` -> `reports/BROKEN_PYTHON_REPAIR_MATRIX.md`

## Hot Files

- `data/upstream_broken_python/mathsquiz/mathsquiz.py`
- `data/upstream_broken_python/mathsquiz/mathsquiz-step2.py`
- `data/upstream_broken_python/mathsquiz/mathsquiz-step3.py`
- `data/upstream_broken_python/polygons/polygons.py`
- `fixed/broken-python/mathsquiz/quiz_core.py`
- `fixed/broken-python/polygons/polygons.py`

## Root Causes

- Original maths quiz script does not compile and contains wrong scoring logic.
- Step 2 and Step 3 use global `score` instead of function parameters.
- Polygon script does not compile and hard-codes incorrect behavior for non-triangle/non-square polygons.

## Fixed Behavior

The fixed copy compiles, is import-safe, separates pure logic from interaction, calculates correct quiz and polygon results, and is covered by before/after tests.
