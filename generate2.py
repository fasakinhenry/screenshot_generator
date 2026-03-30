import os
import subprocess
from pygments import highlight
from pygments.lexers import TextLexer
from pygments.formatters import HtmlFormatter

HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"
WKHTML = "wkhtmltopdf"

def convert(txt_file):
    with open(txt_file) as f:
        content = f.read()

    formatter = HtmlFormatter()
    html = highlight(content, TextLexer(), formatter)

    base = os.path.splitext(os.path.basename(txt_file))[0]
    html_path = os.path.join(HTML_DIR, base + "_out.html")
    pdf_path = os.path.join(PDF_DIR, base + "_out.pdf")

    with open(html_path, "w") as f:
        f.write(html)

    subprocess.run([WKHTML, html_path, pdf_path], check=True)

def main():
    folder = "output_txt"
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            convert(os.path.join(folder, file))

if __name__ == "__main__":
    main()