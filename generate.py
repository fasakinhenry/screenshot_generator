from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
import os
import json
import shutil
import random

# ---- CONFIG ----
SRC_DIR = "input_code"
HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"
CONFIG_FILE = "students.json"

STYLE = "default"
FONT_FAMILY = "Consolas, 'JetBrains Mono', monospace"
FONT_SIZE = "14px"
FONT_WEIGHT = "600"
LINE_HEIGHT = "1.25"
DPI = "400"

HEADER_TEMPLATE = """\
#!/usr/bin/env python3
# NAME: {name}
# MATRIC NO: {mat}
# DEPARTMENT: {dept}
# --------------------------
"""

WKHTML = "wkhtmltopdf"

# ---- RANDOMIZE ----
def generate_efficiencies(seed):
    random.seed(seed)
    return [0.75] + [round(random.uniform(0.70, 0.80), 2) for _ in range(6)]

# ---- HTML ----
def generate_html(py_file, html_path, student_info):
    with open(py_file, "r", encoding="utf-8") as f:
        code = f.read()

    efficiencies = generate_efficiencies(student_info["mat"])

    code = code.replace(
        "efficiencies = [0.75, 0.72, 0.78, 0.74, 0.76, 0.73, 0.77]",
        f"efficiencies = {efficiencies}"
    )

    header_text = HEADER_TEMPLATE.format(**student_info)
    code_with_header = header_text + "\n" + code

    formatter = HtmlFormatter(
        linenos='inline',
        cssclass="highlight",
        style=STYLE
    )

    pygments_css = formatter.get_style_defs('.highlight')

    custom_css = f"""
    <style>
    {pygments_css}

    body {{
        font-family: {FONT_FAMILY};
        margin: 0;
    }}

    .highlight {{
        padding: 10px 15px;
    }}

    .highlight pre {{
        font-size: {FONT_SIZE};
        font-weight: {FONT_WEIGHT};
        line-height: {LINE_HEIGHT};
        white-space: pre-wrap;
        word-break: break-word;
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
    font-size: 13px;
">
File &nbsp; Edit &nbsp; Format &nbsp; Run &nbsp; Options &nbsp; Window &nbsp; Help
</div>

{highlight(code_with_header, PythonLexer(), formatter)}

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

# ---- PDF ----
def generate_pdf(html_path, pdf_path):
    subprocess.run([
        WKHTML,
        "--enable-local-file-access",
        "--disable-smart-shrinking",
        "--dpi", DPI,
        "-s", "A4",
        html_path,
        pdf_path
    ], check=True)

# ---- PROCESS ----
def process_file(py_file, student_info):
    base = os.path.splitext(os.path.basename(py_file))[0]
    html_path = os.path.join(HTML_DIR, base + ".html")
    pdf_path = os.path.join(PDF_DIR, base + ".pdf")

    generate_html(py_file, html_path, student_info)
    generate_pdf(html_path, pdf_path)

# ---- UTILS ----
def clean_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def load_students():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def safe_name(name):
    return name.lower().replace(" ", "_")

def zip_output(student_name):
    zip_name = f"csc_assignment_{safe_name(student_name)}.zip"
    temp = f"temp_{safe_name(student_name)}"
    shutil.copytree(PDF_DIR, temp)
    subprocess.run(["7z", "a", "-tzip", zip_name, temp])
    shutil.rmtree(temp)

# ---- MAIN ----
def main():
    students = load_students()

    for student in students:
        clean_folder(HTML_DIR)
        clean_folder(PDF_DIR)

        for file in os.listdir(SRC_DIR):
            if file.endswith(".py"):
                process_file(os.path.join(SRC_DIR, file), student)

        zip_output(student["name"])

if __name__ == "__main__":
    main()