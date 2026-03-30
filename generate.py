from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
import os
import json
import shutil

# ---- CONFIG ----
SRC_DIR = "input_code"
HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"
CONFIG_FILE = "students.json"

STYLE = "default"
FONT_FAMILY = "Consolas, 'JetBrains Mono', monospace"
FONT_SIZE = "14px"
FONT_WEIGHT = "600"
LINE_HEIGHT = "1.2"
DPI = "400"

HEADER_TEMPLATE = """\
#!/usr/bin/env python3
# NAME: {name}
# MATRIC NO: {mat}
# DEPARTMENT: {dept}
# --------------------------
"""

WKHTML = "wkhtmltopdf"

# ---- FUNCTIONS ----
def generate_html(py_file, html_path, student_info):
    with open(py_file, "r", encoding="utf-8") as f:
        code = f.read()

    header_text = HEADER_TEMPLATE.format(**student_info)
    code_with_header = header_text + "\n" + code

    formatter = HtmlFormatter(linenos='inline', cssclass="highlight", style=STYLE)
    pygments_css = formatter.get_style_defs('.highlight')

    custom_css = f"""
    <style>
    {pygments_css}
    body {{
        font-family: {FONT_FAMILY};
        margin: 20px;
    }}
    .highlight pre {{
        font-size: {FONT_SIZE} !important;
        font-weight: {FONT_WEIGHT} !important;
        line-height: {LINE_HEIGHT} !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }}
    </style>
    """

    html_content = f"""
<html>
<head>{custom_css}</head>
<body>

<div style="
    background: #eeeeee;
    border-bottom: 1px solid #cfcfcf;
    padding: 6px 10px;
    font-family: Consolas, monospace;
    font-size: 13px;
    font-weight: 500;
    color: #000;
">
    File &nbsp; Edit &nbsp; Format &nbsp; Run &nbsp; Options &nbsp; Window &nbsp; Help
</div>

{highlight(code_with_header, PythonLexer(), formatter)}

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_pdf(html_path, pdf_path):
    subprocess.run([
        WKHTML,
        "--enable-local-file-access",
        "--disable-smart-shrinking",
        "--dpi", str(DPI),
        "-s", "A4",
        "-O", "Portrait",
        html_path,
        pdf_path
    ], check=True)


def process_file(py_file, student_info):
    base = os.path.splitext(os.path.basename(py_file))[0]
    html_path = os.path.join(HTML_DIR, base + ".html")
    pdf_path = os.path.join(PDF_DIR, base + ".pdf")
    generate_html(py_file, html_path, student_info)
    generate_pdf(html_path, pdf_path)
    print(f"Created: {pdf_path}")


def clean_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)


def load_students():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_name(name):
    return name.lower().replace(" ", "_")


def zip_output(student_name):
    zip_name = f"csc_assignment_{safe_name(student_name)}.zip"
    # Copy PDF folder temporarily
    temp_folder = f"temp_{safe_name(student_name)}"
    shutil.copytree(PDF_DIR, temp_folder)
    subprocess.run(["7z", "a", "-tzip", zip_name, temp_folder], check=True)
    shutil.rmtree(temp_folder)
    print(f"📦 Created zip: {zip_name}")


def main():
    students = load_students()

    for student in students:
        print(f"\n🚀 Processing student: {student['name']}")
        clean_folder(HTML_DIR)
        clean_folder(PDF_DIR)

        for file in os.listdir(SRC_DIR):
            if file.endswith(".py"):
                full_path = os.path.join(SRC_DIR, file)
                process_file(full_path, student)

        # Remove default unwanted PDFs if any
        for unwanted in ["generate.pdf", "generate2.pdf"]:
            path = os.path.join(PDF_DIR, unwanted)
            if os.path.exists(path):
                os.remove(path)

        # Zip the output
        zip_output(student["name"])


if __name__ == "__main__":
    main()