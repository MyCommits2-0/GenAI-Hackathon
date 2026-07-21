import json

from langchain_ollama import ChatOllama
from prompts import EVALUATION_PROMPT

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def evaluate_submission(student_code, marking_scheme):

    prompt = EVALUATION_PROMPT.format(
        marking_scheme=json.dumps(
            marking_scheme,
            indent=2
        ),
        student_code=student_code[:15000]
    )

    response = llm.invoke(prompt)

    result = response.content

    result = (
        result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        result = json.loads(result)

        criteria = result.get(
            "criteria",
            []
        )

        code_lower = student_code.lower()

        # ----------------------------------------
        # Evidence Based Corrections
        # ----------------------------------------

        for item in criteria:

            section = item.get(
                "section",
                ""
            ).lower()

            max_marks = item.get(
                "max_marks",
                0
            )

            awarded = item.get(
                "awarded_marks",
                0
            )

            # Safety check
            if awarded > max_marks:
                item["awarded_marks"] = max_marks

            # Add Bonus
            if "bonus" in section:

                if "addbonus" not in code_lower:

                    item["awarded_marks"] = 0
                    item["comments"] = (
                        "Bonus functionality not found."
                    )
                    item["evidence"] = []

            # Deduct Salary
            if "deduct" in section:

                if "deduct" not in code_lower:

                    item["awarded_marks"] = 0
                    item["comments"] = (
                        "Salary deduction functionality not found."
                    )
                    item["evidence"] = []

            # Transaction History
            if "transaction" in section:

                if "transaction" not in code_lower:

                    item["awarded_marks"] = 0
                    item["comments"] = (
                        "Transaction history feature not implemented."
                    )
                    item["evidence"] = []

            # Department Report
            if "department" in section:

                if "department" not in code_lower:

                    item["awarded_marks"] = 0
                    item["comments"] = (
                        "Department-wise reporting not found."
                    )
                    item["evidence"] = []

            # Add Employee
            if (
                "add employee" in section
                and "validation" not in section
            ):

                if "addemployee" not in code_lower:

                    item["awarded_marks"] = 0
                    item["comments"] = (
                        "Employee addition functionality not found."
                    )
                    item["evidence"] = []

        # ----------------------------------------
        # Recalculate Total
        # ----------------------------------------

        total_marks = sum(
            item.get(
                "awarded_marks",
                0
            )
            for item in criteria
        )

        result["total_marks"] = total_marks

        # ----------------------------------------
        # Result Classification
        # ----------------------------------------

        if total_marks <= 15:

            result["result"] = "FAIL"

            default_comment = (
                "The submission does not satisfy the minimum exam requirements. "
                "Several core functionalities are missing or incomplete. "
                "The student should focus on implementing all mandatory features "
                "and improving validation logic."
            )

        elif total_marks <= 24:

            result["result"] = "BELOW AVERAGE"

            default_comment = (
                "The submission demonstrates partial implementation of the required "
                "features. Some important functionalities and validation checks are "
                "missing. Additional work is required to improve completeness."
            )

        elif total_marks <= 30:

            result["result"] = "GOOD"

            default_comment = (
                "The submission implements most of the required functionality. "
                "The overall structure is good, though some validations or advanced "
                "features are missing."
            )

        else:

            result["result"] = "VERY GOOD"

            default_comment = (
                "The submission successfully implements nearly all requirements. "
                "The design is clear and functionality is largely complete with only "
                "minor improvements needed."
            )

        # Use model comment if available
        if not result.get(
            "overall_comments"
        ):
            result[
                "overall_comments"
            ] = default_comment

        return result

    except Exception as e:

        return {
            "error": "Invalid JSON returned by model",
            "details": str(e),
            "raw_response": result
        }