# big_integer_square_root_tools

Computes the integer floor of the square root of an arbitrarily large non-negative integer using Newton's method with exact integer division.

```python
from big_integer_square_root_tools import floor_sqrt, floor_sqrt_str

floor_sqrt(10**200)       # 100000000000000000000000000000000000000000000000000
floor_sqrt("123456789012345678901234567890")  # int result, parsed from string
floor_sqrt_str("123456789012345678901234567890")  # string result, no int exposed
```

## Why this exists

Python's `math.isqrt` solves this problem, and does so faster. This library exists for the case where you want the algorithm itself to be inspectable: a single, self-contained Newton iteration with no opaque built-in, suitable for environments where the correctness argument must be auditable in the source rather than trusted to the platform. The trade-off is speed: `math.isqrt` is implemented in C and will outperform this pure-Python version on every input size.

## Edge cases

The function accepts an `int` or a decimal `str`. Strings are stripped of surrounding whitespace before parsing; embedded whitespace, non-decimal characters, and signs other than a single leading `+` are rejected by Python's own `int` parsing and surface as `ValueError`. Negative values raise `ValueError` regardless of input type. Empty and whitespace-only strings raise `ValueError`. Passing a `float` raises `TypeError`.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

