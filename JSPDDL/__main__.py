"""
Paper: "Creating PDDL Models from Javascript using LLMs: Preliminary Results"
Link: https://openreview.net/pdf?id=VyTxXSPmbE

This paper leverages LLMs to translate low-level controller code in the context
of provided NL info about the domain and extrapolate its preconditions and effects
into a PDDL action.

This pipeline consists of two stages:
    1. "Summarization" - sums controller functions
    2. "Extraction" - uses summaries to select appropriate set of types and preicates from allowed set and constructs action using them.
        a) Input controller functions corresponding to some action the bot can undertake
        b) Partial domain model comprising set of allowed predicates and object types
        c) NL domain info necessary to the action. 
        
Outputting PDDL action definitions for each provided controller function.

Case study: Minecraft domain used in "Voyager" (Wang et al. 2023) to generate valid PDDL actions for:
    - Crafting craft table
    - Planks
    - Sticks
    - Wooden sword
"""

import os, json
from l2p import *
from .pipelines.summarization import SummarizationStage
from .pipelines.extraction import ExtractionStage

def run_JSPDDL_pipeline(
        model: LLM, 
        p_action_name: str,
        action_name: str,
        prompts: list[str], 
        func: str, 
        nl_domains: list[str], 
        obj_hierarchy: str, 
        pred_pool: str
        ) -> str:

    sum = SummarizationStage()
    sum.generate_nl_summary(model=model, p_action_name=p_action_name, 
                            js_function=func, prompt=prompts[0])

    p1 = sum.get_p1()
    print(p1)

    sum.generate_goal_pre_eff_summary(model=llm, p_action_name=p_action_name, 
                                      nl_summary=p1, js_function=js_function, prompt=prompts[1])
    p2 = sum.get_p2()
    print(p2)

    ext = ExtractionStage()
    select_types = ext.extract_types(model=model, action_name=action_name, prompt=prompts[2], p1=p1, p2=p2, obj_hierarchy=obj_hierarchy)
    print(select_types)

    select_predicates = ext.extract_predicates()

if __name__ == "__main__":

    # load in model
    engine = "gpt-4o-mini"
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OPENAI(model=engine, api_key=api_key)

    # action name
    parent_action_name = "craftItem"
    action_name = "craftSticks"
    
    # load in js function
    with open("data/04_craftItem.js", "r", encoding="utf-8") as f:
        js_function = f.read()

    # load in NL domain
    with open("data/01_nl_domain_summary.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    craft_item_descriptions = data.get("craftItem", {})
    
    nl_domain_list = [(f'{key}: {description}') for key, description in craft_item_descriptions.items()]

    with open("data/02_object_hierarchy.txt", "r") as f:
        obj_hierarchy = f.read()
    with open("data/03_predicate_pool.txt", "r") as f:
        pred_pool = f.read()

    prompt_1 = load_file(f'prompt_templates/p1.txt')
    prompt_2 = load_file(f'prompt_templates/p2.txt')
    prompt_3 = load_file(f'prompt_templates/p3.txt')
    prompt_4 = load_file(f'prompt_templates/p4.txt')
    prompt_5 = load_file(f'prompt_templates/p5.txt')

    prompts = [prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]


    run_JSPDDL_pipeline(
        model=llm, 
        p_action_name=parent_action_name,
        action_name=action_name,
        prompts=prompts, 
        func=js_function, 
        nl_domains=nl_domain_list,
        obj_hierarchy=obj_hierarchy,
        pred_pool=pred_pool)

