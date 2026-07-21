import zipfile
import os
import json

SUPPORTED_EXTENSIONS = (
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".txt",
    ".md"
)

def load_marking_scheme(file_path):

    with open(file_path, "r") as f:
        return json.load(f) 
def extract_zip(zip_path, extract_dir="extracted"):

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    return extract_dir


def load_submission_code(extract_dir):

    all_code = []

    for root, dirs, files in os.walk(extract_dir):

        for file in files:

            if file.endswith(SUPPORTED_EXTENSIONS):

                file_path = os.path.join(root, file)

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        content = f.read()

                        all_code.append(
                            f"\n\nFILE: {file}\n"
                            f"{content}"
                        )

                except Exception as e:

                    print(
                        f"Error reading {file}: {e}"
                    )

    return "\n".join(all_code)