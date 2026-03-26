from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from agent.agent import run_agent
import os

app = Flask(__name__)
UPLOAD_DIR = "uploads"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = ""
    uploaded_file = None

    if request.content_type and "application/json" in request.content_type:
        data = request.get_json(silent=True) or {}
        user_input = data.get("message", "").strip()
    else:
        user_input = request.form.get("message", "").strip()
        uploaded_file = request.files.get("file")

    upload_note = ""
    if uploaded_file and uploaded_file.filename:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = secure_filename(uploaded_file.filename)
        if not filename:
            return jsonify({"error": "Invalid file name"}), 400

        saved_path = os.path.join(UPLOAD_DIR, filename)
        uploaded_file.save(saved_path)
        run_agent(f"read {saved_path}")
        upload_note = f"Loaded file: {filename}. "

    if not user_input:
        if upload_note:
            return jsonify({"response": upload_note + "Ask a question about the uploaded file."})
        return jsonify({"error": "Empty message"}), 400

    response = run_agent(user_input)
    if upload_note:
        response = upload_note + response

    return jsonify({"response": response})

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    app.run(debug=True, port=5000)
