import unittest

from big_integer_square_root_tools import floor_sqrt, floor_sqrt_str


class FloorSqrtTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(floor_sqrt(0), 0)

    def test_one(self):
        self.assertEqual(floor_sqrt(1), 1)

    def test_small_perfect_squares(self):
        self.assertEqual(floor_sqrt(4), 2)
        self.assertEqual(floor_sqrt(9), 3)
        self.assertEqual(floor_sqrt(100), 10)

    def test_small_non_squares(self):
        # 2 -> floor is 1, 3 -> 1
        self.assertEqual(floor_sqrt(2), 1)
        self.assertEqual(floor_sqrt(3), 1)
        # 8 -> 2, 15 -> 3, 35 -> 5
        self.assertEqual(floor_sqrt(8), 2)
        self.assertEqual(floor_sqrt(15), 3)
        self.assertEqual(floor_sqrt(35), 5)

    def test_large_perfect_square(self):
        n = 10**200
        k = 10**100
        self.assertEqual(floor_sqrt(n), k)

    def test_large_just_below_square(self):
        k = 10**100
        self.assertEqual(floor_sqrt(k * k - 1), k - 1)

    def test_large_just_above_square(self):
        k = 10**100
        self.assertEqual(floor_sqrt(k * k + 1), k)

    def test_huge_non_square(self):
        # A number with many digits whose floor sqrt is known by construction.
        target = 10**250 + 17  # arbitrary, odd, huge
        self.assertEqual(floor_sqrt(target), 10**125)

    def test_string_input_basic(self):
        self.assertEqual(floor_sqrt("9"), 3)
        self.assertEqual(floor_sqrt("17"), 4)

    def test_string_input_huge(self):
        k = 10**50
        self.assertEqual(floor_sqrt(str(k * k)), k)

    def test_string_input_with_whitespace(self):
        self.assertEqual(floor_sqrt("  49  "), 7)

    def test_negative_int_raises(self):
        with self.assertRaises(ValueError):
            floor_sqrt(-1)

    def test_negative_string_raises(self):
        with self.assertRaises(ValueError):
            floor_sqrt("-1")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            floor_sqrt("")

    def test_whitespace_only_string_raises(self):
        with self.assertRaises(ValueError):
            floor_sqrt("   ")

    def test_type_error_for_float(self):
        with self.assertRaises(TypeError):
            floor_sqrt(2.0)

    def test_floor_sqrt_str_returns_string(self):
        self.assertEqual(floor_sqrt_str("100"), "10")

    def test_floor_sqrt_str_huge(self):
        k = 10**100
        self.assertEqual(floor_sqrt_str(str(k * k)), str(k))


if __name__ == "__main__":
    unittest.main()
