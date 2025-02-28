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
        self.selected_types = None
        self.selected_preds = None
        self.extracted_action = None
        self.extracted_predicate = None
    
    def extract_types(self, model, action_name, prompt, nl_domain,
                      p1, p2, obj_hierarchy):
        """Step 3"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{nl_domain}", nl_domain)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{object_hierarchy}", obj_hierarchy)

        types, _ = self.d_b.extract_type(
            model=model,
            domain_desc="",
            prompt_template=prompt
        )

        self.selected_types = types

    def extract_predicates(self, model, action_name, prompt, nl_domain,
                           p1, p2, pred_list):
        """Step 4"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{nl_domain}", nl_domain)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{predicate_list}", pred_list)

        predicates, _ = self.d_b.extract_predicates(
            model=model,
            domain_desc="",
            prompt_template=prompt
            )
        
        self.selected_preds = predicates


    def extract_pddl_action(self, 
                            model, 
                            action_name, 
                            prompt,
                            nl_domain,
                            p1,
                            p2,
                            types, 
                            pred_list):
        """Step 5"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{nl_domain}", nl_domain)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{p3}", types)
        prompt = prompt.replace("{p4}", pred_list)

        action, _, _  = self.d_b.extract_pddl_action(
            model=model,
            domain_desc="",
            prompt_template=prompt,
            action_name=""
        )

        self.extracted_action = action

    def get_types(self):
        return self.selected_types
    
    def get_predicates(self):
        return self.selected_preds
    
    def get_action(self):
        return self.extracted_action

if __name__ == "__main__":
    pass