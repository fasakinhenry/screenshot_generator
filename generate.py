from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
import os
import json
import shutil
import random
import tempfile

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

# ---- RUN CODE AND CAPTURE OUTPUT ----
def run_code_and_capture_output(code_string):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(code_string)
        temp_path = temp_file.name
    try:
        result = subprocess.run(["python", temp_path], capture_output=True, text=True)
        return result.stdout
    finally:
        os.remove(temp_path)

# ---- GENERATE CODE PDF ----
def generate_code_pdf(code, student_info, base_name):
    header_text = HEADER_TEMPLATE.format(**student_info)
    code_with_header = header_text + "\n" + code

    formatter = HtmlFormatter(linenos='inline', cssclass="highlight", style=STYLE)
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
<head>
<meta charset="UTF-8">
{custom_css}
</head>
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

    html_path = os.path.join(HTML_DIR, base_name + ".html")
    pdf_path = os.path.join(PDF_DIR, base_name + ".pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    generate_pdf(html_path, pdf_path)

# ---- GENERATE OUTPUT PDF ----
def generate_output_pdf(output_text, base_name):
    html_path = os.path.join(HTML_DIR, base_name + "_out.html")
    pdf_path = os.path.join(PDF_DIR, base_name + "_out.pdf")

    terminal_header = f"$ python {base_name}.py\n\n"

    html = f"""
<html>
<head>
<meta charset="UTF-8">
</head>
<body style="margin:0; font-family: Consolas, monospace;">
<div style="
    background: #eeeeee;
    padding:15px;
    font-size:14px;
    white-space:pre-wrap;
">
{terminal_header}{output_text}
</div>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    generate_pdf(html_path, pdf_path)

# ---- GENERATE PDF FROM HTML ----
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

# ---- PROCESS ONE FILE FOR ONE STUDENT ----
def process_file(py_file, student_info):
    base_name = os.path.splitext(os.path.basename(py_file))[0]

    with open(py_file, "r", encoding="utf-8") as f:
        code = f.read()

    # inject student-specific efficiencies
    efficiencies = generate_efficiencies(student_info["mat"])
    code = code.replace(
        "efficiencies = [0.75, 0.72, 0.78, 0.74, 0.76, 0.73, 0.77]",
        f"efficiencies = {efficiencies}"
    )

    # generate code PDF
    generate_code_pdf(code, student_info, base_name)

    # run the code and generate output PDF
    output_text = run_code_and_capture_output(code)
    generate_output_pdf(output_text, base_name)

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
        print(f"Processing {student['name']}...")
        clean_folder(HTML_DIR)
        clean_folder(PDF_DIR)

        for py_file in os.listdir(SRC_DIR):
            if py_file.endswith(".py"):
                process_file(os.path.join(SRC_DIR, py_file), student)

        zip_output(student["name"])
        print(f"Done {student['name']}!\n")

if __name__ == "__main__":
    main()