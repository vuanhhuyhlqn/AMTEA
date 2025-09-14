from .AbstractPrompt import AbstractPrompt
from utils.utils import get_code
import os

class UpdatePrompt(AbstractPrompt):
    def __init__(self, good_solver_history, bad_solver_history, mode = "balanced", prompt_name = "update"):
        super().__init__(prompt_name)
        
        self.build(good_solver_history, bad_solver_history, mode)
        
    def build(self, good_solver_history, bad_solver_history, mode):
        prompt_parts = []
        prompt_parts.append(
            "I am solving optimization problems using evolutionary algorithms.\n"
            "The goal is to design generation solvers that take a population of parent solutions and produce an offspring population.\n"
        )

        prompt_parts.append("I have a list of well-performing solvers with their descriptions, modes, and Python code implementations as follows:\n")
        for idx, solver in enumerate(good_solver_history, 1):
            prompt_parts.append(
                f"No.{idx} solver’s description, mode and its code:\n"
                f"# Mode: {solver.mode}\n"
                f"# Its Description\n{{{solver.algorithm}}}\n"
                "# Its Python Code Implementation of a Function\n"
                f"{get_code(solver.id)}\n"
            )
            
        if bad_solver_history:
            prompt_parts.append("\nPoor solvers to avoid with their modes:\n")
            for idx, solver in enumerate(bad_solver_history, 1):
                prompt_parts.append(
                    f"No.{idx} poor solver’s description, mode and its code:\n"
                    f"# Mode: {solver.mode}\n"
                    f"# Its Description\n{{{solver.algorithm}}}\n"
                    "# Its Python Code Implementation of a Function\n"
                    f"{get_code(solver.id)}\n"
                )

        if mode == "exploit":
            prompt_parts.append(
                "\nPlease create a new generation solver that strongly focuses on exploitation "
                "(fast convergence), refining promising regions and reducing diversity while avoiding premature stagnation.\n"
            )
        elif mode == "explore":
            prompt_parts.append(
                "\nPlease create a new generation solver that strongly focuses on exploration "
                "(diversity and coverage), expanding search space and avoiding local minima.\n"
            )
        else:
            prompt_parts.append(
                "\nPlease create a new generation solver that balances exploitation and exploration "
                "to achieve stable progress and maintain diversity.\n"
            )

        prompt_parts.append(
            "Important requirement:\n"
            "- Implement the new solver in Python in a single code block suitable for a file named `solver.py`.\n"
            "- It is allowed and recommended to define multiple helper functions (for example custom crossover, mutation, parameter adaptation…) inside the same code block.\n"
            "- The main entry point must be a function named `generation(population: np.ndarray)` which returns an array of shape (N,d) with offspring values in [0,1].\n"
            "- Combine, hybridize, or extend ideas in a novel way (for example adaptive parameters, multi-point operations, hierarchical selection).\n"
            "- Use clear function names for helper functions.\n\n"
            "First, describe the design idea and main steps of your solver in one sentence inside curly braces outside the code implementation.\n"
            "Then implement the full Python code (helper functions + main `generation`) in one code block.\n"
            "Do not give additional explanations."
        )

        prompt_content = "\n".join(prompt_parts)
        
        prompts_folder = 'LLM/prompts/texts'
        os.makedirs(prompts_folder, exist_ok=True)
        prompt_file = os.path.join(prompts_folder, 'update.txt')
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        
    def get_prompt(self):
        return super().get_prompt()
        
