from agent.planner import decide_action
from tools.calculator import calculate
from tools.search import search
from tools.file_reader import read_file
from llm.llm import ask_llm, summarize_pdf
from agent.memory import Memory

memory = Memory()

def log(text):
    with open("logs/agent_logs.txt", "a") as f:
        f.write(text + "\n")

def run_agent(user_input):

    print("\n[Agent Thinking...]")
    log(f"User: {user_input}")
    memory.add_message("user", user_input)

    action = decide_action(user_input)
    print("Action decided:", action)
    log(f"Action: {action}")

    if action == "calculator":
        expr = user_input.replace("calculate", "")
        result = calculate(expr)

    elif action == "search":
        keyword = user_input.replace("find", "").strip()
        text = memory.document
        result = search(text, keyword)

    elif action == "read_file":
        file_path = user_input.replace("read", "", 1).strip() or "data/sample.txt"
        text = read_file(file_path)
        memory.set_document(text)
        result = f"Document loaded into memory from: {file_path}"

    elif action == "summarize_pdf":
        file_path = user_input.replace("summarize pdf", "", 1).strip()
        if not file_path:
            result = "Please provide a PDF path, e.g. summarize pdf data/sample_pdf.pdf"
        else:
            result = summarize_pdf(file_path)

    else:
        result = ask_llm(user_input)

    log(f"Result: {result}")
    memory.add_message("assistant", result, action=action)
    return result