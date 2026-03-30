from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
import os

# ---- CONFIG ----
SRC_DIR = "input_code"
HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"

STYLE = "default"
FONT_FAMILY = "Consolas, 'JetBrains Mono', monospace"
FONT_SIZE = "14px"
FONT_WEIGHT = "600"
LINE_HEIGHT = "1.2"
DPI = "400"

STUDENT_INFO = {
    "name": "OLOGUNORE HONOUR AYOMIKUN", 
    "mat": "SEN/24/9518",
    "dept": "SOFTWARE ENGINEERING"
}

HEADER_TEMPLATE = """\
#!/usr/bin/env python3
# NAME: {name}
# MATRIC NO: {mat}
# DEPARTMENT: {dept}
# --------------------------
"""

WKHTML = "wkhtmltopdf"

# ---- SETUP DIRECTORIES ----
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# ---- FUNCTIONS ----
def generate_html(py_file, html_path, student_info):
    with open(py_file, "r", encoding="utf-8") as f:
        code = f.read()

    header_text = HEADER_TEMPLATE.format(**student_info)
    code_with_header = header_text + "\n" + code

    formatter = HtmlFormatter(linenos='inline', cssclass="highlight", style=STYLE)
    pygments_css = formatter.get_style_defs('.highlight')

    filename = os.path.basename(py_file)

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
        "--dpi", DPI,
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


def main():
    for file in os.listdir(SRC_DIR):
        if file.endswith(".py"):
            # process_file(file, STUDENT_INFO)
            full_path = os.path.join(SRC_DIR, file)
            process_file(full_path, STUDENT_INFO)


if __name__ == "__main__":
    main()