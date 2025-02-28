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
from l2p import *
from .pipelines import extraction, summarization

engine = "gpt-4o-mini"
api_key = os.environ.get("OPENAI_API_KEY")
llm = OPENAI(model=engine, api_key=api_key)

def run_JSPDDL_pipeline():
    pass

if __name__ == "__main__":
    pass