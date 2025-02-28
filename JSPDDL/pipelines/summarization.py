"""
Stage one of JS-PDDL pipeline: summarizes provided function implementing an action
    - Javascript function implementing an action w/ output are 2 NL summaries describing function:
        1. Giving general overview (concise, high-level 3-5 line summary of function)
        2. Elucidating action goals, preconditions, and effects in NL (targeted 1-sentence summary of 25 words or less)
    - To produce summary (1): LLM provided w/ prompt containing instructions and function implementation
    - To produce summary (2): LLM provided w/ function implementation and summary (1)
"""
import os
from l2p import *

engine = "gpt-4o-mini"
api_key = os.environ.get("OPENAI_API_KEY")
llm = OPENAI(model=engine, api_key=api_key)

class SummarizationStage:

    def __init__(self):
        self.nl_summary = ""
        self.nl_pred_summary = ""
    
    def generate_nl_summary(self, model, p_action_name, js_function, prompt):
        """Step 1"""
        prompt = prompt.replace("{p_action_name}", p_action_name)
        prompt = prompt.replace("{javascript_function}", js_function)
        nl_func_summary = model.query(prompt=prompt)
        self.nl_summary = nl_func_summary

    def generate_goal_pre_eff_summary(self, model, p_action_name, nl_summary, js_function, prompt):
        """Step 2"""
        prompt = prompt.replace("{p_action_name}", p_action_name)
        prompt = prompt.replace("{javascript_function}", js_function)
        prompt = prompt.replace("{p1}", nl_summary)
        nl_action_summary = model.query(prompt=prompt)
        self.nl_pred_summary = nl_action_summary

    def get_p1(self):
        return self.nl_summary
    
    def get_p2(self):
        return self.nl_pred_summary

if __name__ == "__main__":
    with open("data/craftItem.js", "r", encoding="utf-8") as f:
        js_function = f.read()

    prompt_1 = load_file(f'prompt_templates/p1.txt')
    prompt_2 = load_file(f'prompt_templates/p2.txt')

    sum = SummarizationStage()
    sum.generate_nl_summary(model=llm, js_function=js_function, prompt=prompt_1)

    p1 = sum.get_p1()
    print(p1)

    sum.generate_goal_pre_eff_summary(model=llm, nl_summary=p1, js_function=js_function, prompt=prompt_2)
    p2 = sum.get_p2()
    print(p2)