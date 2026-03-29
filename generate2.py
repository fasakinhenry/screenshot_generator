import os
import subprocess
from datetime import datetime
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
import argparse

# ----------------- CONFIG -----------------
HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"

ALLOWED_EXTENSIONS = [".py", ".js", ".java", ".c", ".cpp", ".txt"]

STYLE = "friendly"
FONT_FAMILY = "'JetBrains Mono', Consolas, monospace"
FONT_SIZE = "14px"
FONT_WEIGHT = "600"
LINE_HEIGHT = "1.4"
DPI = 400

WKHTML = "wkhtmltopdf"

# Student info template
STUDENT_INFO = {
    "name": "Alice",
    "matric": "12345",
    "department": "CS"
}

HEADER_TEMPLATE = """\
NAME: {name}
MATRIC NO: {matric}
DEPARTMENT: {department}
File: {filename}
Generated: {timestamp}
--------------------------
"""

# ----------------- SETUP DIRECTORIES -----------------
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# ----------------- FUNCTIONS -----------------
def generate_html(file_path, html_path, student_info):
    """Generate syntax-highlighted HTML with student info header."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    # Header
    header_text = HEADER_TEMPLATE.format(
        name=student_info.get("name", ""),
        matric=student_info.get("matric", ""),
        department=student_info.get("department", ""),
        filename=os.path.basename(file_path),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    header_text = ''
    code_with_header = header_text + "\n" + code

    # Lexer detection
    try:
        lexer = get_lexer_for_filename(file_path)
    except Exception:
        lexer = TextLexer()

    # Pygments formatter
    formatter = HtmlFormatter(
        linenos=None,
        cssclass="highlight",
        style=STYLE
    )
    pygments_css = formatter.get_style_defs('.highlight')

    # Custom CSS
    custom_css = f"""
    <style>
    {pygments_css}
    body {{
        font-family: {FONT_FAMILY};
        margin: 10px;
        border: solid 1px #777;
    }}
    .highlight pre {{
        font-size: {FONT_SIZE} !important;
        font-weight: {FONT_WEIGHT} !important;
        line-height: {LINE_HEIGHT} !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
        background-color: #fff !important;
        padding-left: 5px;
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
        <p style="padding-left:5px;">Python 3.13.9 (tags/v3.13.9:8183fa5, Oct 14 2025, 14:09:13) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.</p>

        {highlight(code_with_header, lexer, formatter)}
    </body>
    </html>
    """

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_pdf(html_path, pdf_path):
    """Convert HTML to PDF using wkhtmltopdf."""
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


def process_file(file_path, student_info):
    base = os.path.splitext(os.path.basename(file_path))[0]
    html_path = os.path.join(HTML_DIR, base + "_output" + ".html")
    pdf_path = os.path.join(PDF_DIR, base + "_output" + ".pdf")

    generate_html(file_path, html_path, student_info)
    generate_pdf(html_path, pdf_path)
    print(f"Created: {pdf_path}")


def find_files(directories, extensions):
    """Recursively search directories for allowed files."""
    found = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for f in files:
                if any(f.endswith(ext) for ext in extensions):
                    found.append(os.path.join(root, f))
    return found


# ----------------- MAIN -----------------
def main():
    parser = argparse.ArgumentParser(description="Generate PDFs from source code with headers.")
    parser.add_argument(
        "-d", "--dirs",
        nargs="+",
        default=["."],
        help="Directories to search for source files (default = current directory)"
    )
    args = parser.parse_args()

    files_to_process = find_files(args.dirs, ALLOWED_EXTENSIONS)

    if not files_to_process:
        print("No source files with allowed extensions found.")
        return

    for file_path in files_to_process:
        process_file(file_path, {})

    print("All files processed.")


if __name__ == "__main__":
    main()