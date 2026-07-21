import os
import json
from datetime import datetime


def generate_report(
        result,
        output_file="reports/evaluation_report.md"
):

    # Create reports folder if not exists
    report_dir = os.path.dirname(output_file)

    if report_dir and not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # -------------------------------
    # Markdown Report
    # -------------------------------
    report = []

    report.append("# Student Evaluation Report\n")

    report.append(
        f"Generated: {datetime.now()}\n"
    )

    report.append(
        f"## Total Marks: "
        f"{result['total_marks']}/40\n"
    )

    report.append(
        "## Overall Comments\n"
    )

    report.append(
        result["overall_comments"]
    )

    report.append("\n---\n")

    for item in result["criteria"]:

        report.append(
            f"## {item['section']}"
        )

        report.append(
            f"Marks: "
            f"{item['awarded_marks']}"
            f"/{item['max_marks']}"
        )

        report.append("\nEvidence:")

        if item["evidence"]:

            for ev in item["evidence"]:
                report.append(f"- {ev}")

        else:
            report.append("- No evidence found")

        report.append(
            f"\nComments: "
            f"{item['comments']}\n"
        )

        report.append("\n")

    report_text = "\n".join(report)

    # Save Markdown Report
    with open(
            output_file,
            "w",
            encoding="utf-8"
    ) as f:

        f.write(report_text)

    # -------------------------------
    # JSON Report
    # -------------------------------
    json_file = os.path.join(
        report_dir,
        "evaluation_report.json"
    )

    with open(
            json_file,
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    print(f"Markdown Report: {output_file}")
    print(f"JSON Report: {json_file}")

    return {
        "markdown_report": output_file,
        "json_report": json_file
    }