import os
import subprocess

HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"
WKHTML = "wkhtmltopdf"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def generate_html(txt_file, html_path):
    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    html = f"""
<html>
<body style="margin:0; font-family: Consolas, monospace;">

<div style="
    background:black;
    color:#00ff00;
    padding:15px;
    font-size:14px;
    white-space:pre-wrap;
    min-height:100vh;
">
{content}
</div>

</body>
</html>
"""

    with open(html_path, "w") as f:
        f.write(html)

def generate_pdf(html, pdf):
    subprocess.run([
        WKHTML,
        "--enable-local-file-access",
        html,
        pdf
    ], check=True)

def main():
    for file in os.listdir("output_txt"):
        if file.endswith(".txt"):
            base = file.replace(".txt", "")
            html = os.path.join(HTML_DIR, base + "_out.html")
            pdf = os.path.join(PDF_DIR, base + "_out.pdf")

            generate_html(os.path.join("output_txt", file), html)
            generate_pdf(html, pdf)

if __name__ == "__main__":
    main()