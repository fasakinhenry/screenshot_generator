from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess
import os
import json
import shutil
import random

SRC_DIR = "input_code"
HTML_DIR = "html_temp"
PDF_DIR = "pdf_output"
OUTPUT_TXT_DIR = "output_txt"
CONFIG_FILE = "students.json"

WKHTML = "wkhtmltopdf"

HEADER_TEMPLATE = """\
#!/usr/bin/env python3
# NAME: {name}
# MATRIC NO: {mat}
# DEPARTMENT: {dept}
# --------------------------
"""

# ---------- HELPERS ----------

def load_students():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def clean_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def safe_name(name):
    return name.lower().replace(" ", "_")

# ---------- RANDOMIZATION ----------

def generate_efficiencies():
    values = [0.75]
    for _ in range(6):
        values.append(round(random.uniform(0.70, 0.80), 2))
    return values

def inject_efficiencies(code, efficiencies):
    new_line = f"efficiencies = {efficiencies}"
    lines = code.split("\n")

    return "\n".join(
        new_line if line.strip().startswith("efficiencies") else line
        for line in lines
    )

def create_temp_code(original_file, student):
    with open(original_file) as f:
        code = f.read()

    efficiencies = generate_efficiencies()
    modified = inject_efficiencies(code, efficiencies)

    temp_file = f"temp_{student['mat'].replace('/', '_')}.py"

    with open(temp_file, "w") as f:
        f.write(modified)

    return temp_file

# ---------- PDF ----------

def generate_html(py_file, html_path, student):
    with open(py_file) as f:
        code = f.read()

    header = HEADER_TEMPLATE.format(**student)
    code = header + "\n" + code

    formatter = HtmlFormatter(linenos=True)
    html = f"<style>{formatter.get_style_defs()}</style>" + highlight(code, PythonLexer(), formatter)

    with open(html_path, "w") as f:
        f.write(html)

def generate_pdf(html, pdf):
    subprocess.run([WKHTML, html, pdf], check=True)

# ---------- MAIN ----------

def main():
    students = load_students()

    for student in students:
        print(f"\n🚀 {student['name']}")

        clean_folder(HTML_DIR)
        clean_folder(PDF_DIR)
        clean_folder(OUTPUT_TXT_DIR)

        for file in os.listdir(SRC_DIR):
            if file.endswith(".py"):
                full = os.path.join(SRC_DIR, file)

                temp = create_temp_code(full, student)

                base = os.path.splitext(file)[0]

                html = os.path.join(HTML_DIR, base + ".html")
                pdf = os.path.join(PDF_DIR, base + ".pdf")
                out_txt = os.path.join(OUTPUT_TXT_DIR, base + ".txt")

                generate_html(temp, html, student)
                generate_pdf(html, pdf)

                result = subprocess.run(["python", temp], capture_output=True, text=True)
                with open(out_txt, "w") as f:
                    f.write(result.stdout)

                os.remove(temp)

        # Convert outputs to PDF
        subprocess.run(["python", "generate2.py", "-d", OUTPUT_TXT_DIR])

        # Zip
        zip_name = f"csc_assignment_{safe_name(student['name'])}"
        shutil.copytree(PDF_DIR, zip_name)
        subprocess.run(["7z", "a", f"{zip_name}.zip", zip_name])
        shutil.rmtree(zip_name)

        print(f"✅ Done: {zip_name}.zip")

if __name__ == "__main__":
    main()