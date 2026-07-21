from parser import *
from evaluator import *
from report_generator import *
import os

MARKING_SCHEME = "marking_scheme.json"

print("=" * 60)
print(" SUNBEAM LAB EXAM EVALUATION ASSISTANT ")
print("=" * 60)

zip_file = input(
    "\nEnter Student ZIP File Path: "
).strip()

if not os.path.exists(zip_file):
    print(f"\n[ERROR] File not found: {zip_file}")
    exit()

try:

    print("\n[1] Loading Student Submission...")

    extract_dir = extract_zip(
        zip_file
    )

    student_code = load_submission_code(
        extract_dir
    )

    print("[OK] Submission Loaded")

    print("\n[2] Loading Marking Scheme...")

    scheme = load_marking_scheme(
        MARKING_SCHEME
    )

    print("[OK] Marking Scheme Loaded")

    print("\n[3] Evaluating Submission...")

    result = evaluate_submission(
        student_code,
        scheme
    )

    print("[OK] Evaluation Complete")

    total_possible = sum(
        item["marks"]
        for item in scheme["criteria"]
    )

    print("\n" + "=" * 60)
    print(" EVALUATION SUMMARY ")
    print("=" * 60)

    print(
        f"\nTotal Marks: "
        f"{result['total_marks']}/{total_possible}"
    )

    print(
        f"\nOverall Comments:\n"
        f"{result['overall_comments']}"
    )

    print("\n[4] Generating Reports...")

    reports = generate_report(
        result
    )

    print("\n[OK] Reports Generated")

    print(
        f"\nMarkdown Report : "
        f"{reports['markdown_report']}"
    )

    print(
        f"JSON Report     : "
        f"{reports['json_report']}"
    )

    print("\nDone.")

except Exception as e:

    print(
        f"\n[ERROR] {str(e)}"
    )