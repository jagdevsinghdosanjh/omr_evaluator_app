import json

# Load answer key from JSON file
def load_answer_key(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Compare extracted answers with correct answers
def compare_answers(detected_answers, correct_answers):
    result = {
        "total_questions": len(correct_answers),
        "correct": 0,
        "incorrect": 0,
        "unmarked": 0,
        "details": []
    }

    for q_num, correct_option in correct_answers.items():
        marked_option = detected_answers.get(q_num, "Unmarked")
        if marked_option == "Unmarked":
            result["unmarked"] += 1
            status = "Unmarked"
        elif marked_option == correct_option:
            result["correct"] += 1
            status = "Correct"
        else:
            result["incorrect"] += 1
            status = "Incorrect"

        result["details"].append({
            "question": q_num,
            "marked": marked_option,
            "correct": correct_option,
            "status": status
        })

    return result
