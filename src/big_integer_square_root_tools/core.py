from __future__ import annotations

import math

from typing import Union

Number = Union[int, str]


def floor_sqrt(value: Number) -> int:
    """Return floor(sqrt(value)) for a non-negative, arbitrarily large integer.

    *value* may be given as an int or as a decimal string.  Passing a string is
    useful when the caller already holds the number as text (file input, command
    lines, audit logs) so they need not first materialise a huge Python int
    just to hand it over.

    Newton's method is used with exact integer division.  The iteration is the
    familiar ``x_{n+1} = (x_n + n // x_n) // 2``; the termination condition is
    ``x_{n+1} >= x_n`` (equivalently ``x_n - x_{n+1} <= 1``), which is exact
    for non-negative integers and provably yields the floor of the true square
    root.  No floating point arithmetic is used at any point.

    Raises:
        TypeError: if *value* is not an int or str.
        ValueError: if *value* is negative or if a string does not parse as a
            non-negative decimal integer.
    """
    if isinstance(value, str):
        n = _parse_decimal(value)
    elif isinstance(value, int):
        if value < 0:
            raise ValueError("floor_sqrt is defined only for non-negative integers")
        n = value
    else:  # pragma: no cover - exercised by the TypeError test
        raise TypeError("floor_sqrt expects an int or a decimal string")

    return _floor_sqrt(n)


def floor_sqrt_str(value: str) -> str:
    """Convenience wrapper: parse *value* as a decimal string and return the
    result as a decimal string.  No intermediate int is ever exposed to the
    caller.
    """
    n = _parse_decimal(value)
    return str(_floor_sqrt(n))


def _parse_decimal(value: str) -> int:
    stripped = value.strip()
    if not stripped:
        raise ValueError("empty string is not a valid non-negative integer")
    # Python's int() already rejects embedded whitespace, signs other than a
    # single leading +, and any non-digit characters.  We add an explicit
    # negative check so the error message is consistent with the int path.
    if stripped[0] == "-":
        raise ValueError("floor_sqrt is defined only for non-negative integers")
    n = int(stripped, 10)
    if n < 0:  # pragma: no cover - int() with base 10 cannot produce negative here
        raise ValueError("floor_sqrt is defined only for non-negative integers")
    return n


def _floor_sqrt(n: int) -> int:
    if n < 2:
        # Covers 0 and 1 directly: sqrt(0)=0, sqrt(1)=1.  Skipping the
        # Newton iteration here also avoids the degenerate initial guess of 0
        # for n == 1, which would divide by zero.
        return n

    # Initial guess: use math.isqrt when available (Python 3.8+) for a tight
    # starting point.  math.isqrt itself computes the floor square root, so
    # we could return it directly -- but we re-derive via Newton so the code
    # path and its correctness argument are self-contained and auditable in
    # one place.
    x = n.bit_length()
    # A power of two strictly greater than sqrt(n).  Cheaper and simpler than
    # a floating estimate, and perfectly adequate for the iteration.
    x = 1 << ((x + 1) >> 1)

    while True:
        y = (x + n // x) >> 1
        if y >= x:
            break
        x = y

    return x
