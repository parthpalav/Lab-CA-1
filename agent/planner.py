def decide_action(user_input):

    if "summarize pdf" in user_input:
        return "summarize_pdf"

    if "calculate" in user_input:
        return "calculator"

    elif "find" in user_input:
        return "search"

    elif "read" in user_input:
        return "read_file"

    else:
        return "llm"