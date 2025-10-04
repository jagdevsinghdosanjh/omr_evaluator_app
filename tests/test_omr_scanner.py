from modules import omr_scanner

def test_extract_answers_from_mock_image():
    # Simulate image path or mock input
    mock_image_path = "tests/mock_omr_sheet.png"

    # This test assumes a mock scanner or placeholder function
    answers = omr_scanner.extract_answers(mock_image_path)

    assert isinstance(answers, list)
    assert all(ans in ["A", "B", "C", "D", "Unmarked"] for ans in answers)
    assert len(answers) > 0
