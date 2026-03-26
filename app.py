from flask import Flask, request, jsonify, render_template
from agent.agent import run_agent
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
    response = run_agent(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True, port=5000)
