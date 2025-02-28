"""
Stage two of JS-PDDL pipeline: contains two sub-stages
    1. Selects appropriate types and predicates for target action from provided pool via Codestral-22B-v0.1 prompting P3+P4
        - Prompts P3 
"""

OBJECT_HIERARCHY = ""
PREDICATE_POOL = """
(agent located at ?agent - player ?square - gridSquare)
(object located at ?item - some object ?square - gridSquare)
(connected ?current position - gridSquare ?next position - gridSquare)
(HasWoodBlock ?agent - player ?wood - woodBlock)
(HasPlankBlock ?agent - player ?plank - plankBlock)
(HasStickItem ?agent - player ?stick - stickItem)
(HasWoodenSword ?agent - player ?sword - woodenSword)
(HasWoodenPickaxe ?agent - player ?pickaxe - woodenPickaxe)
(HasCraftTable ?agent - player ?table - craftTable)
"""
NL_DOMAIN_INFO = ""

class ExtractionStage:
    
    def extract_types(self, model, prompt):
        """Step 3"""
        pass

    def extract_predicates(self, model, prompt):
        """Step 4"""
        pass

    def extract_pddl_action(self, model, types, predicates, prompt):
        """Step 5"""
        pass

if __name__ == "__main__":
    pass