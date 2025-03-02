"""
Stage two of JS-PDDL pipeline: contains two sub-stages
    1. Selects appropriate types and predicates for target action from provided pool via Codestral-22B-v0.1 prompting P3+P4
    2. Prompts LLM to construct action from P3 (selected types) and P4 (selected predicates)
"""

class ExtractionStage:
    
    def extract_types(self, model, domain_builder, prompt, action_name, action_desc,
                      p1, p2, obj_hierarchy):
        """Step 3"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{action_desc}", action_desc)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{object_hierarchy}", obj_hierarchy)

        types, output = domain_builder.extract_type(
            model=model,
            domain_desc="",
            prompt_template=prompt
        )

        return types, output

    def extract_predicates(self, model, domain_builder, prompt, action_name, 
                           action_desc, p1, p2, pred_pool):
        """Step 4"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{action_desc}", action_desc)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{predicate_list}", pred_pool)

        predicates, output = domain_builder.extract_predicates(
            model=model,
            domain_desc="",
            prompt_template=prompt
            )
        
        return predicates, output


    def extract_pddl_action(self, model, domain_builder, prompt, action_name, 
                            action_desc, p1, p2, types, pred_pool):
        """Step 5"""
        prompt = prompt.replace("{action_name}", action_name)
        prompt = prompt.replace("{action_desc}", action_desc)
        prompt = prompt.replace("{p1}", p1)
        prompt = prompt.replace("{p2}", p2)
        prompt = prompt.replace("{p3}", types)
        prompt = prompt.replace("{p4}", pred_pool)

        action, _, output, _  = domain_builder.extract_pddl_action(
            model=model,
            domain_desc="",
            prompt_template=prompt,
            action_name=action_name
        )

        return action, output