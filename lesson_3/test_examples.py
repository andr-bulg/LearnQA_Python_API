class TestExample:
    def test_check_math(self):
        a = 5
        b = 9
        expected_sum = 14
        assert a + b == expected_sum, f"Сумма переменных a и b не равна {expected_sum}"

    def test_check_math_2(self):
        a = 5
        b = 11
        expected_sum = 14
        assert a + b == expected_sum, f"Сумма переменных a и b не равна {expected_sum}"


