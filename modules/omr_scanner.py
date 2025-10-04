import cv2
import numpy as np
from PIL import Image
import tempfile

def extract_answers(uploaded_file):
    # Step 1: Convert uploaded image to OpenCV format
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    image = cv2.imread(tmp_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)[1]

    # Step 2: Detect contours (bubbles)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubbles = [cnt for cnt in contours if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 1000]

    # Step 3: Sort bubbles top-to-bottom, left-to-right
    def sort_contours(cnts):
        bounding_boxes = [cv2.boundingRect(c) for c in cnts]
        cnts, _ = zip(*sorted(zip(cnts, bounding_boxes), key=lambda b: (b[1][1], b[1][0])))
        return cnts

    sorted_bubbles = sort_contours(bubbles)

    # Step 4: Analyze filled bubbles
    answers = {}
    question_number = 1
    options = ['A', 'B', 'C', 'D']

    for i in range(0, len(sorted_bubbles), 4):
        group = sorted_bubbles[i:i+4]
        filled = None
        for j, cnt in enumerate(group):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [cnt], -1, 255, -1)
            total = cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=mask))
            if total > 200:  # Threshold for filled bubble
                filled = options[j]
        answers[f"Q{question_number}"] = filled if filled else "Unmarked"
        question_number += 1

    return answers
