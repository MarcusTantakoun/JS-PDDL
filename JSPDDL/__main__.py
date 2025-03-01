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

import os
from l2p.llm_builder import LLM, OPENAI
from l2p.domain_builder import DomainBuilder
from l2p.utils import load_file
from .pipelines.summarization import SummarizationStage
from .pipelines.extraction import ExtractionStage

REQUIREMENTS = [
        ":strips",
        ":typing",
        ":equality",
        ":negative-preconditions",
        ":disjunctive-preconditions",
        ":universal-preconditions",
        ":conditional-effects",
    ]

UNSUPPORTED_KEYWORDS = ["object", "pddl", "lisp"]

def run_JSPDDL_pipeline(
        model: LLM, 
        p_action_name: str,
        action_name: str,
        prompts: list[str], 
        func: str, 
        nl_domains: list[str], 
        obj_hierarchy: str, 
        pred_pool: str,
        output_dir: str
        ) -> str:

    sum = SummarizationStage()
    ext = ExtractionStage()
    domain_builder = DomainBuilder()

    sum.generate_nl_summary(model=model, p_action_name=p_action_name, 
                            js_function=func, prompt=prompts[0])

    p1 = sum.get_p1()

    sum.generate_goal_pre_eff_summary(model=llm, p_action_name=p_action_name, 
                                      nl_summary=p1, js_function=func, prompt=prompts[1])
    p2 = sum.get_p2()

    ext.extract_types(model=model, action_name=action_name, nl_domain=nl_domains[2], 
                      prompt=prompts[2], p1=p1, p2=p2, obj_hierarchy=obj_hierarchy)
    select_types = ext.get_types()
    types_str = "\n".join(f"- {item}" for item in select_types)

    ext.extract_predicates(model=model, action_name=action_name, prompt=prompts[3], 
                           nl_domain=nl_domains[2], p1=p1, p2=p2, pred_list=pred_pool)
    select_predicates = ext.get_predicates()
    predicates_str = "\n".join(
        [pred["clean"].replace(":", " ; ") for pred in select_predicates]
    )

    ext.extract_pddl_action(model=model, action_name=action_name,
                            prompt=prompts[4], nl_domain=nl_domains[2], p1=p1, p2=p2, 
                            types=types_str, pred_list=predicates_str)
    action = ext.get_action()

    generate_action(
        domain_builder=domain_builder,
        action=action,
        output=output_dir
        )

def generate_action(domain_builder, action, output):
    
    desc = ""
    desc += domain_builder.action_desc(action)

    # write the PDDL domain to the file
    with open(output, "w", encoding="utf-8") as f:
        f.write(desc)


def get_prompts() -> list[str]:
    prompt_1 = load_file(f'prompt_templates/p1.txt')
    prompt_2 = load_file(f'prompt_templates/p2.txt')
    prompt_3 = load_file(f'prompt_templates/p3.txt')
    prompt_4 = load_file(f'prompt_templates/p4.txt')
    prompt_5 = load_file(f'prompt_templates/p5.txt')

    return [prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]


def get_assumptions(func_dir, nl_domain_dir, p_action: str, obj_hierarchy_dir, predicates_dir,):
    js_func = load_file(func_dir)
    nl_domain = load_file(nl_domain_dir)
    descriptions = nl_domain.get(p_action, {})
    nl_domain_list = [(f'{key}: {description}') for key, description in descriptions.items()]
    obj_hierarchy = load_file(obj_hierarchy_dir)
    pred_pool = load_file(predicates_dir)

    assumptions = {
        "js_func": js_func,
        "nl_domain": nl_domain_list,
        "object_hierarchy": obj_hierarchy,
        "predicate_pool": pred_pool
    }

    return assumptions


if __name__ == "__main__":

    # load in model
    engine = "gpt-4o-mini"
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OPENAI(model=engine, api_key=api_key)

    # action name
    parent_action_name = "craftItem"
    action_name = "craftSticks"

    assumptions = get_assumptions(
        func_dir="data/04_craftItem.js",
        nl_domain_dir="data/01_nl_domain_summary.json",
        p_action=parent_action_name,
        obj_hierarchy_dir="data/02_object_hierarchy.txt",
        predicates_dir="data/03_predicate_pool.txt"
    )

    prompts = get_prompts()
    
    output_dir = "results/craftItem/02_domain.txt"

    run_JSPDDL_pipeline(
        model=llm, 
        p_action_name=parent_action_name,
        action_name=action_name,
        prompts=prompts, 
        func=assumptions['js_func'], 
        nl_domains=assumptions['nl_domain'],
        obj_hierarchy=assumptions['object_hierarchy'],
        pred_pool=assumptions['predicate_pool'],
        output_dir=output_dir)

