import tkinter as tk
from tkinter import filedialog, messagebox

# Try importing PyPDF2 safely
try:
    import PyPDF2
except:
    print("PyPDF2 not installed. Run: pip install PyPDF2")


required_skills = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "html": ["html"],
    "css": ["css"],
    "sql": ["sql"]
}

# Extract PDF text safely


def extract_text_from_pdf(path):
    text = ""
    try:
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content
    except Exception as e:
        messagebox.showerror("PDF Error", str(e))
    return text


def detect_sections(text):
    sections = ["education", "skills", "projects", "experience"]
    result = {}
    text = text.lower()

    for sec in sections:
        result[sec] = sec in text

    return result


def analyze_skills(text):
    text = text.lower()
    found = []
    missing = []

    for skill, keywords in required_skills.items():
        if any(k in text for k in keywords):
            found.append(skill)
        else:
            missing.append(skill)

    return found, missing


def calculate_score(found, sections):
    skill_score = (len(found) / len(required_skills)) * 50
    section_score = (sum(sections.values()) / len(sections)) * 50
    return round(skill_score + section_score, 2)


def generate_suggestions(score, missing, sections):
    suggestions = []

    if score < 50:
        suggestions.append("Improve resume by adding more skills/projects.")

    if missing:
        suggestions.append("Add missing skills: " + ", ".join(missing[:3]))

    for sec, present in sections.items():
        if not present:
            suggestions.append(f"Include '{sec}' section.")

    return suggestions


def analyze_resume():
    path = file_path.get().strip()

    if not path:
        messagebox.showerror("Error", "Please select a file first!")
        return

    try:
        if path.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

        if not text:
            messagebox.showerror("Error", "No text found in file!")
            return

        sections = detect_sections(text)
        found, missing = analyze_skills(text)
        score = calculate_score(found, sections)
        suggestions = generate_suggestions(score, missing, sections)

        result_text.delete("1.0", tk.END)

        result_text.insert(tk.END, f"Score: {score}%\n\n")

        result_text.insert(tk.END, "Skills Found:\n")
        for s in found:
            result_text.insert(tk.END, f"- {s}\n")

        result_text.insert(tk.END, "\nMissing Skills:\n")
        for s in missing:
            result_text.insert(tk.END, f"- {s}\n")

        result_text.insert(tk.END, "\nSections:\n")
        for sec, val in sections.items():
            result_text.insert(tk.END, f"- {sec}: {'Yes' if val else 'No'}\n")

        result_text.insert(tk.END, "\nSuggestions:\n")
        for s in suggestions:
            result_text.insert(tk.END, f"- {s}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def browse_file():
    path = filedialog.askopenfilename(
        filetypes=[("All files", "*.txt *.pdf")]
    )
    file_path.set(path)


# GUI STARTS HERE (VERY IMPORTANT)
root = tk.Tk()
root.title("Resume Analyzer AI")
root.geometry("650x500")

file_path = tk.StringVar()

tk.Label(root, text="Resume Analyzer AI", font=("Arial", 16)).pack(pady=10)

tk.Entry(root, textvariable=file_path, width=60).pack(pady=5)

tk.Button(root, text="Browse", command=browse_file).pack(pady=5)
tk.Button(root, text="Analyze Resume", command=analyze_resume).pack(pady=10)

result_text = tk.Text(root, height=20, width=80)
result_text.pack(pady=10)

root.mainloop()
