from sa.nodes.report import calculate_grade

def test_calculate_grade():
    assert calculate_grade(95) == "A"
    assert calculate_grade(90) == "A"
    assert calculate_grade(89.9) == "B"
    assert calculate_grade(75) == "C"
    assert calculate_grade(60) == "D"
    assert calculate_grade(59) == "F"
