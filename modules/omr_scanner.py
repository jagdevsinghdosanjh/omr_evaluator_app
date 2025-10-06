import cv2
import numpy as np
import tempfile
import os

def extract_answers(uploaded_file, filled_threshold=150, debug=False):
    # Step 1: Convert uploaded image to OpenCV format
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    image = cv2.imread(tmp_path)
    if image is None:
        raise ValueError("Failed to load image. Ensure the file is a valid image format.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 2: Adaptive thresholding for better scan resilience
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # Step 3: Detect contours (bubbles)
    contours_info = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_info) < 2:
        raise ValueError("Contour extraction failed: insufficient return values.")

    contours = contours_info[-2]  # Compatible with OpenCV 3 and 4

    # Expanded area range for flexible bubble detection
    bubbles = [cnt for cnt in contours if 50 < cv2.contourArea(cnt) < 3000]

    if not bubbles:
        raise ValueError("No valid bubbles detected. Try adjusting scan quality or threshold settings.")

    # Step 4: Sort bubbles top-to-bottom, left-to-right
    def sort_contours(cnts):
        bounding_boxes = [cv2.boundingRect(c) for c in cnts]
        sorted_pairs = sorted(zip(cnts, bounding_boxes), key=lambda b: (b[1][1], b[1][0]))
        return [cnt for cnt, _ in sorted_pairs]

    sorted_bubbles = sort_contours(bubbles)

    # Step 5: Analyze filled bubbles
    answers = {}
    question_number = 1
    options = ['A', 'B', 'C', 'D']

    for i in range(0, len(sorted_bubbles), 4):
        group = sorted_bubbles[i:i+4]
        if len(group) < 4:
            continue  # Skip incomplete question groups

        filled = None
        confidences = []

        for j, cnt in enumerate(group):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [cnt], -1, 255, -1)
            total = cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=mask))
            confidences.append(total)
            if total > filled_threshold:
                filled = options[j]

        if debug:
            print(f"Q{question_number} bubble fill levels: {confidences}")

        answers[f"Q{question_number}"] = filled if filled else "Unmarked"
        question_number += 1

    # Step 6: Check if all answers are unmarked
    if all(ans == "Unmarked" for ans in answers.values()):
        raise ValueError("No answers detected. Please check the scan quality or alignment.")

    # Cleanup temp file
    os.remove(tmp_path)

    return answers
