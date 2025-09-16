from .AbstractPrompt import AbstractPrompt
from utils.utils import get_code
import os

class UpdatePrompt(AbstractPrompt):
    def __init__(self, good_solver_history, bad_solver_history, alpha, prompt_name = "update"):
        super().__init__(prompt_name)
        
        self.build(good_solver_history, bad_solver_history, alpha)
        
    def build(self, good_solver_history, bad_solver_history, alpha):
        prompt_parts = []
        prompt_parts.append(
            "I am solving optimization problems using evolutionary algorithms.\n"
            "The goal is to design generation solvers that take a population of parent solutions and produce an offspring population.\n"
        )

        prompt_parts.append("I have a list of well-performing solvers with their descriptions, alpha, and Python code implementations as follows:\n")
        for idx, solver in enumerate(good_solver_history, 1):
            prompt_parts.append(
                f"No.{idx} solver’s description, alpha and its code:\n"
                f"# alpha: {solver.alpha}\n"
                f"# Its Description\n{{{solver.algorithm}}}\n"
                "# Its Python Code Implementation of a Function\n"
                f"{get_code(solver.id)}\n"
            )
            
        if bad_solver_history:
            prompt_parts.append("\nPoor solvers to avoid with their alphas:\n")
            for idx, solver in enumerate(bad_solver_history, 1):
                prompt_parts.append(
                    f"No.{idx} poor solver’s description, alpha and its code:\n"
                    f"# alpha: {solver.alpha}\n"
                    f"# Its Description\n{{{solver.algorithm}}}\n"
                    "# Its Python Code Implementation of a Function\n"
                    f"{get_code(solver.id)}\n"
                )

        # if mode == "exploit":
        #     prompt_parts.append(
        #         "\nPlease create a new generation solver that strongly focuses on exploitation "
        #         "(fast convergence), refining promising regions and reducing diversity while avoiding premature stagnation.\n"
        #     )
        # elif mode == "explore":
        #     prompt_parts.append(
        #         "\nPlease create a new generation solver that strongly focuses on exploration "
        #         "(diversity and coverage), expanding search space and avoiding local minima.\n"
        #     )
        # else:
        #     prompt_parts.append(
        #         "\nPlease create a new generation solver that balances exploitation and exploration "
        #         "to achieve stable progress and maintain diversity.\n"
        #     )

        prompt_parts.append(
            "I will give you a parameter alpha ∈ [0,1].\n"
            "- If alpha = 0 → the solver must behave as pure exploration (maximize diversity, disruptive crossover, strong mutation, random injections).\n"
            "- If alpha = 1 → the solver must behave as pure exploitation (focus on elites, mild mutation, local refinement).\n"
            "- Values between 0 and 1 represent a blend, interpolating between exploration and exploitation, the solver's behavior must lean toward the closer extreme.\n"
            f"Here's the value: alpha = {alpha:.5f}\n"
        )

        prompt_parts.append(
            "First, describe the design idea and main steps of your solver in one sentence.\n"
            "The description must be inside a brace outside the code implementation.\n"
            "Next, implement it in Python as a function named `generation`.\n"
            "This function should accept only 1 input: `population`, an array of shape (N, d) of real-valued vectors.\n"
            "The function should return 1 output: `offspring`, an array of shape (N, d) of real-valued vectors.\n"
            "The offspring must stay within the bounds [0, 1] for each variable.\n\n"
            "Do not give additional explanations."
        )

        prompt_content = "\n".join(prompt_parts)
        
        prompts_folder = 'LLM/prompts/texts'
        os.makedirs(prompts_folder, exist_ok=True)
        prompt_file = os.path.join(prompts_folder, 'update.txt')
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        
    def get_prompt(self):
        # print(super().get_prompt())
        return super().get_prompt()
        
