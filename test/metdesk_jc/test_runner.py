import unittest

from metdesk_jc.runner import convert_temperature, get_outliers


class TestTemperatureConverter(unittest.TestCase):
    def test_convert_temperature_shorthand(self):
        self.assertEqual(convert_temperature(25, "c"), 25)
        self.assertEqual(convert_temperature(32, "f"), 0.0)
        self.assertEqual(convert_temperature(25, "k"), 298.15)

    def test_convert_temperature_longhand(self):
        self.assertEqual(convert_temperature(25, "celsius"), 25)
        self.assertEqual(convert_temperature(32, "fahrenheit"), 0.0)
        self.assertEqual(convert_temperature(25, "kelvin"), 298.15)

    def test_convert_temp_unknown_unit(self):
        with self.assertRaises(ValueError):
            convert_temperature(25, "X")


class TestGetOutliers(unittest.TestCase):
    def test_get_outliers_returns_outlier_values(self):
        self.assertListEqual(get_outliers([1, 1, 2, 1, 50, 51], 1), [50, 51])

    def test_get_outliers_returns_empty_array_when_no_outliers(self):
        self.assertListEqual(get_outliers([1, 1, 2, 1, 50], 2), [])

    def test_get_outliers_throws_an_error_when_list_has_a_string(self):
        with self.assertRaises(TypeError):
            get_outliers(["1", 1], 2)

    def test_get_outliers_throws_an_error_when_multiple_is_not_a_number(self):
        with self.assertRaises(TypeError):
            get_outliers([1, 1], "2")


if __name__ == "__main__":
    unittest.main()
