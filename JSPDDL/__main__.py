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

Results found in results/craftItem
"""

import os
from l2p.llm_builder import LLM, OPENAI
from l2p.domain_builder import DomainBuilder
from l2p.utils import load_file
from .pipelines.summarization import SummarizationStage
from .pipelines.extraction import ExtractionStage


def run_JSPDDL_pipeline(
        s_1_model: LLM,
        s_2_model: LLM,
        prompts: list[str], 
        p_action_name: str,
        action_name: str,
        action_desc: str,
        func: str,
        obj_hierarchy: str, 
        pred_pool: str,
        output_dir: str
        ) -> str:
    """Main function to run JSPDDL pipeline"""

    sum = SummarizationStage()          # initialize summarization stage class
    ext = ExtractionStage()             # initialize extraction stage class
    domain_builder = DomainBuilder()    # initialize l2p builder class

    log = "\n\nLLM OUTPUTS:" # logging string for output

    # SUMMARIZATION STAGE
    # Stage 1
    p1 = sum.generate_nl_summary(s_1_model, prompts['p1'], p_action_name, func)
    log += f"\n\n[STAGE ONE OUTPUT]:\n{p1}"

    # Stage 2
    p2 = sum.generate_goal_pre_eff_summary(s_1_model, prompts['p2'], p_action_name, func, p1)
    log += f"\n\n[STAGE TWO OUTPUT]:\n{p2}"

    # EXTRACTION STAGE
    # Stage 3
    select_types, llm_output = ext.extract_types(s_2_model, domain_builder, prompts['p3'], 
                                                 action_name, action_desc, p1, p2, obj_hierarchy)

    types_str = "\n".join(f"- {item}" for item in select_types)
    log += f"\n\n[STAGE THREE OUTPUT]:\n{llm_output}"

    # Stage 4
    select_predicates, llm_output = ext.extract_predicates(s_2_model, domain_builder, prompts['p4'], 
                                                           action_name, action_desc, p1, p2, pred_pool)
    
    predicates_str = "\n".join(
        [pred["clean"].replace(":", " ; ") for pred in select_predicates]
    )
    log += f"\n\n[STAGE FOUR OUTPUT]:\n{llm_output}"

    # Stage 5
    action, llm_output = ext.extract_pddl_action(s_2_model, domain_builder, prompts['p5'], action_name, 
                                                 action_desc, p1, p2, types_str, predicates_str)
    
    log += f"\n\n[STAGE FIVE OUTPUT]:\n{llm_output}"

    generate_action(domain_builder, action, log, output_dir) # parse action together


def generate_action(domain_builder, action, log, output_dir):
    """Parse whole action together and log to output directory"""
    desc = "```\n"
    desc += domain_builder.action_desc(action)
    desc += "\n```"
    desc += log

    with open(output_dir, "w") as f:
        f.write(desc)


def get_prompts():
    """Retrieve all prompts into list"""
    prompts = {
        "p1": load_file(f'prompt_templates/p1.txt'),
        "p2": load_file(f'prompt_templates/p2.txt'),
        "p3": load_file(f'prompt_templates/p3.txt'),
        "p4": load_file(f'prompt_templates/p4.txt'),
        "p5": load_file(f'prompt_templates/p5.txt')
    }

    return prompts


def get_assumptions(func_dir, nl_domain_dir, p_action: str, obj_hierarchy_dir, predicates_dir,):
    """Retrieves all assumptions and put it into dictionary"""

    js_func = load_file(func_dir)
    nl_domain = load_file(nl_domain_dir)
    descriptions = nl_domain.get(p_action, {})
    nl_domain_list = [{key: description} for key, description in descriptions.items()]
    obj_hierarchy = load_file(obj_hierarchy_dir)
    pred_pool = load_file(predicates_dir)

    assumptions = {
        "js_func": js_func,
        "nl_domain_list": nl_domain_list,
        "object_hierarchy": obj_hierarchy,
        "predicate_pool": pred_pool
    }

    return assumptions


if __name__ == "__main__":

    # load in model
    engine = "gpt-4o"
    api_key = os.environ.get("OPENAI_API_KEY")

    p_action_name = "craftItem" # parent action name

    # load in assumptions
    assumptions = get_assumptions(
        func_dir="data/04_craftItem.js",                    # javascript function
        nl_domain_dir="data/01_nl_domain_summary.json",     # NL domain
        p_action=p_action_name,                             # parent action name
        obj_hierarchy_dir="data/02_object_hierarchy.txt",   # object type hierarchy
        predicates_dir="data/03_predicate_pool.txt"         # predicate pool
    )

    prompts = get_prompts() # load in prompts

    # iterate through each action in parent function
    for i in assumptions['nl_domain_list']:
        action_name = list(i.keys())[0]
        action_desc = list(i.values())[0]

        for j in range(3):

            stage_1_llm = OPENAI(model=engine, api_key=api_key, temperature=0.3)
            stage_2_llm = OPENAI(model=engine, api_key=api_key, temperature=0.5)
            
            # set output directory
            output_dir = f"results/craftItem/{action_name}/attempt_{j}.txt"
            os.makedirs(os.path.dirname(output_dir), exist_ok=True)

            run_JSPDDL_pipeline(
                s_1_model=stage_1_llm,
                s_2_model=stage_2_llm, 
                prompts=prompts,
                p_action_name=p_action_name,
                action_name=action_name,
                action_desc=action_desc, 
                func=assumptions['js_func'], 
                obj_hierarchy=assumptions['object_hierarchy'],
                pred_pool=assumptions['predicate_pool'],
                output_dir=output_dir)

