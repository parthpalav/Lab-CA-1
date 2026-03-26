from agent.agent import run_agent

print("=== Agentic AI Research Assistant ===")

while True:
    user = input("\nYou: ")
    response = run_agent(user)
    print("Agent:", response)