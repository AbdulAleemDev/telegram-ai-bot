from app.graph.agent import run_agent

# Test FAQ tool
result = run_agent("What payment methods do you accept?")
print("FAQ Test:", result)

# Test ticket tool
result2 = run_agent("My product arrived damaged, I want a refund")
print("Ticket Test:", result2)