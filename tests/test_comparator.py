from modules import comparator

def test_compare_answers():
    student_answers = ["A", "B", "C", "D", "Unmarked"]
    correct_answers = ["A", "C", "C", "D", "A"]

    result = comparator.compare_answers(student_answers, correct_answers)
    assert result["correct"] == 3
    assert result["incorrect"] == 1
    assert result["unmarked"] == 1
    assert result["total_questions"] == 5
    assert len(result["details"]) == 5
