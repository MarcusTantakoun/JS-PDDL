"""
Stage one of JS-PDDL pipeline: summarizes provided function implementing an action
    - Javascript function implementing an action w/ output are 2 NL summaries describing function:
        1. Giving general overview (concise, high-level 3-5 line summary of function)
        2. Elucidating action goals, preconditions, and effects in NL (targeted 1-sentence summary of 25 words or less)
    - To produce summary (1): LLM provided w/ prompt containing instructions and function implementation
    - To produce summary (2): LLM provided w/ function implementation and summary (1)
"""


class SummarizationStage:
    
    def generate_nl_summary(self, model, prompt):
        """Step 1"""
        nl_func_summary = model.query(prompt=prompt)

    def generate_goal_pre_eff_summary(self, model, prompt):
        """Step 2"""
        nl_action_summary = model.query(prompt=prompt)

if __name__ == "__main__":
    pass