import streamlit as st
import tempfile
import os

from parser import *
from evaluator import *
from report_generator import *

MARKING_SCHEME = "marking_scheme.json"

st.set_page_config(
    page_title="Sunbeam Lab Evaluation Assistant",
    layout="wide"
)

st.title("🎓 Sunbeam Lab Exam Evaluation Assistant")

st.write(
    "Upload a student's ZIP submission and generate an AI-based evaluation report."
)

uploaded_file = st.file_uploader(
    "Upload Student ZIP",
    type=["zip"]
)

if uploaded_file:

    temp_dir = tempfile.mkdtemp()

    zip_path = os.path.join(
        temp_dir,
        uploaded_file.name
    )

    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Evaluate Submission"):

        try:

            with st.spinner(
                "Evaluating submission..."
            ):

                extract_dir = extract_zip(
                    zip_path,
                    os.path.join(
                        temp_dir,
                        "extracted"
                    )
                )

                student_code = load_submission_code(
                    extract_dir
                )

                scheme = load_marking_scheme(
                    MARKING_SCHEME
                )

                result = evaluate_submission(
                    student_code,
                    scheme
                )

                total_possible = sum(
                    item["marks"]
                    for item in scheme["criteria"]
                )

                st.success(
                    "Evaluation Completed"
                )

                st.metric(
                    "Total Marks",
                    f"{result['total_marks']}/{total_possible}"
                )

                st.subheader(
                    "Overall Comments"
                )

                st.write(
                    result["overall_comments"]
                )

                st.subheader(
                    "Section Wise Evaluation"
                )

                for item in result["criteria"]:

                    with st.expander(
                        item["section"]
                    ):

                        st.write(
                            f"Marks: "
                            f"{item['awarded_marks']}"
                            f"/{item['max_marks']}"
                        )

                        st.write(
                            "Comments:"
                        )

                        st.info(
                            item["comments"]
                        )

                        st.write(
                            "Evidence:"
                        )

                        if item["evidence"]:

                            for ev in item["evidence"]:
                                st.write(
                                    f"• {ev}"
                                )

                        else:
                            st.write(
                                "No evidence found"
                            )

                reports = generate_report(
                    result
                )

                st.subheader(
                    "Generated Reports"
                )

                with open(
                    reports["markdown_report"],
                    "rb"
                ) as f:

                    st.download_button(
                        "Download Markdown Report",
                        f,
                        file_name="evaluation_report.md"
                    )

                with open(
                    reports["json_report"],
                    "rb"
                ) as f:

                    st.download_button(
                        "Download JSON Report",
                        f,
                        file_name="evaluation_report.json"
                    )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )