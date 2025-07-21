from agents.semantic import interpret_prompt
from agents.logic import generate_app_logic
from agents.visual import generate_ui
from agents.deploy import deploy_to_targets
from memory.kernel import load_user_profile

class Str8ZeroCore:
    def __init__(self, user_context, prompt):
        self.memory = load_user_profile(user_context)
        self.intent = interpret_prompt(prompt)
        self.logic = generate_app_logic(self.intent)
        self.visual = generate_ui(self.intent)
        self.deployment = deploy_to_targets(self.logic, self.visual, self.memory)

    def build(self):
        return {
            "intent": self.intent,
            "logic": self.logic,
            "visual": self.visual,
            "deployment": self.deployment
        }
