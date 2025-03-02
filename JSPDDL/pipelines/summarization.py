"""
Stage one of JS-PDDL pipeline: summarizes provided function implementing an action
    - Javascript function implementing an action w/ output are 2 NL summaries describing function:
        1. Giving general overview (concise, high-level 3-5 line summary of function)
        2. Elucidating action goals, preconditions, and effects in NL (targeted 1-sentence summary of 25 words or less)
    - To produce summary (1): LLM provided w/ prompt containing instructions and function implementation
    - To produce summary (2): LLM provided w/ function implementation and summary (1)
"""

class SummarizationStage:
    
    def generate_nl_summary(self, model, prompt, p_action_name, js_function):
        """Step 1"""
        prompt = prompt.replace("{p_action_name}", p_action_name)
        prompt = prompt.replace("{javascript_function}", js_function)

        nl_func_summary = model.query(prompt=prompt)
        return nl_func_summary

    def generate_goal_pre_eff_summary(self, model, prompt, p_action_name, js_function, p1):
        """Step 2"""
        prompt = prompt.replace("{p_action_name}", p_action_name)
        prompt = prompt.replace("{javascript_function}", js_function)
        prompt = prompt.replace("{p1}", p1)

        nl_action_summary = model.query(prompt=prompt)
        return nl_action_summary