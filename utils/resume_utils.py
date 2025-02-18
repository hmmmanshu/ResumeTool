import subprocess
from datetime import datetime

def generate_pdf_from_latex(resume_code):
    print("Generating pdf from latex")
    resume_code = cleanup_resume_text(resume_code)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    tex_file = filename+".tex"
    pdf_file = filename+".pdf"
    with open(tex_file, "w") as f:
        f.write(resume_code)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file])

    # Cleanup
    files = ['.tex', '.aux', '.log', '.out']
    for file in files:
        subprocess.call([f"rm ./{filename}{file}"], shell=True)
    
    print(f"PDF generated: {pdf_file}")
    return pdf_file


def cleanup_resume_text(resume_code):
    resume_code = resume_code.replace('```latex','').replace('```','')
    resume_code = resume_code.split('end{document}')[0]+'end{document}'
    return resume_code