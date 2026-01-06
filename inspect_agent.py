from agno.agent import Agent
import inspect

print("Agent Init Signature:")
print(inspect.signature(Agent.__init__))

print("\nAgent Class Docstring:")
print(Agent.__doc__)
