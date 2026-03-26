import google.generativeai as genai
from config import GEMINI_API_KEY
from tools.file_reader import extract_text_from_pdf

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def ask_llm(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM error: {e}"


def summarize_pdf(file_path):
    if not file_path.lower().endswith(".pdf"):
        return "Summary error: Please provide a valid .pdf file path."

    try:
        extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        return f"Summary error: {e}"

    trimmed_note = ""
    safe_limit = 30000
    if len(extracted_text) > safe_limit:
        extracted_text = extracted_text[:safe_limit]
        trimmed_note = "\n\nNote: The document was trimmed to 30,000 characters due to length."

    prompt = (
        "You are given document content extracted from a PDF. "
        "Summarize it clearly and concisely.\n\n"
        "Requirements:\n"
        "1. Provide a concise summary of the document's main topic and purpose.\n"
        "2. Highlight key points, findings, or arguments.\n"
        "3. Keep the summary digestible and well structured.\n\n"
        "Document content:\n"
        f"{extracted_text}"
        f"{trimmed_note}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Summary API error: {e}"