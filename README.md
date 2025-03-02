# {JS-PDDL}
This is a paper recreation "Creating PDDL Models from Javascript using LLMs: Preliminary Results" (Sikes et al. 2024) using **Language-to-Plan (L2P)** 

[Original Paper Link](https://openreview.net/pdf?id=VyTxXSPmbE)

[L2P library GitHub link](https://github.com/AI-Planning/l2p/tree/main)

## Recreation
This Github recreates the major components of what we coin "JS-PDDL" framework where the LLM decomposes natural language information from operational models via Javascript functions. This then translates it into action PDDL specifications.

Specifically, this recreation only tests out the Minecraft domain – `craftItem` Javascript operational function model; which is then deconstructed into (4) actions:
- crafting-table
- sticks
- wooden-planks
- wooden-sword
