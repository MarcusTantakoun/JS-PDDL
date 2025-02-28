"""
Stage two of JS-PDDL pipeline: contains two sub-stages
    1. Selects appropriate types and predicates for target action from provided pool via Codestral-22B-v0.1 prompting P3+P4
        - Prompts P3 
"""

from l2p import DomainBuilder
from l2p.utils import format_types

UNSUPPORTED_KEYWORDS = ["object", "pddl", "lisp"]

class ExtractionStage:

    def __init__(self):
        self.d_b = DomainBuilder()
        self.selected_types = ""
        self.selected_preds = ""
        self.pddl_action = ""
    
    def extract_types(self, model, action_name, prompt, p1, p2, obj_hierarchy):
        """Step 3"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{object_hierarchy}", obj_hierarchy)
        types, _ = self.d_b.extract_type(
            model=model,
            domain_desc="",
            prompt_template=prompt
        )

        return types

    def extract_predicates(self, model, prompt):
        """Step 4"""
        self.d_b.extract_predicates()

    def extract_pddl_action(self, model, types, predicates, prompt):
        """Step 5"""
        self.d_b.extract_pddl_sction()

if __name__ == "__main__":
    pass