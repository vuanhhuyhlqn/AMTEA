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

        prompt_parts.append("I have a list of well-performing solvers with their descriptions, and Python code implementations as follows:\n")
        for idx, solver in enumerate(good_solver_history[:3], 1):
            prompt_parts.append(
                f"No.{idx} solver’s description, alpha and its code:\n"
                f"# alpha: {solver.alpha}\n"
                f"# Its Description\n{{{solver.algorithm}}}\n"
                "# Its Python Code Implementation of a Function\n"
                f"{get_code(solver.id)}\n"
            )
            
        if bad_solver_history:
            prompt_parts.append("Poor solvers to avoid with their alphas:\n")
            for idx, solver in enumerate(bad_solver_history[:3], 1):
                prompt_parts.append(
                    f"No.{idx} poor solver’s description, alpha and its code:\n"
                    f"# alpha: {solver.alpha}\n"
                    f"# Its Description\n{{{solver.algorithm}}}\n"
                    "# Its Python Code Implementation of a Function\n"
                    f"{get_code(solver.id)}\n"
                )

        prompt_parts.append(
            "I will give you a parameter alpha ∈ [0,1].\n"
            "- If alpha = 0 → the solver must behave as pure exploration (maximize diversity, disruptive crossover, strong mutation, random injections).\n"
            "- If alpha = 1 → the solver must behave as pure exploitation (focus on elites, mild mutation, local refinement).\n"
            "- Values between 0 and 1 represent a blend, the solver must lean toward the nearest extreme. Do not invert this interpretation!\n"
            f"Here's the value: alpha = {alpha:.4f}\n"
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
            
    def build2(self, good_solver_history, bad_solver_history, alpha):
        prompt_parts = []
        prompt_parts.append(
            "I am solving optimization problems using evolutionary algorithms.\n"
            "The goal is to design generation solvers that take a population of parent solutions and produce an offspring population.\n"
        )

        prompt_parts.append("I have compiled a list of case studies from previous runs to provide insight into successful and unsuccessful solvers. Use these principles as inspiration and avoid their pitfalls.\n")
        prompt_parts.append("Case Studies of Successful Solvers:\n")
        prompt_parts.append("Principle 1 (Alpha: 0.85): A hybrid GA solver that uses a mild Simulated Binary Crossover (SBX) for exploitation and an adaptive Polynomial Mutation where mutation strength decreases as the population converges, ensuring local refinement.\n")
        prompt_parts.append("Principle 2 (Alpha: 0.20): A Differential Evolution (DE) solver that emphasizes exploration by using the DE/rand/1 mutation and injecting completely random solutions into the population to maintain diversity when the search stagnates.\n")
        prompt_parts.append("Principle 3 (Alpha: 0.50): A balanced approach that combines a one-point crossover for global search with a strong, adaptive Gaussian mutation to encourage significant exploration across the search space.\n")
        prompt_parts.append("Principle 4 (Alpha: 0.95): A swarm-based solver that focuses on exploiting the best solutions found so far by creating new individuals that are linear combinations of the current individual and the best individual in the population.\n")
        for idx, solver in enumerate(good_solver_history[:3], 1):
            prompt_parts.append(
                f"Principle {idx + 5}: (Alpha: {solver.alpha}) {solver.algorithm}\n"
            )
            
        if bad_solver_history:
            prompt_parts.append("\nCase Studies of Poor Solvers (to avoid):\n")
            prompt_parts.append("Pitfall 1 (Alpha: 0.25): A solver that relies on an overly aggressive Polynomial Mutation with a high mutation strength, leading to the destruction of promising solutions and an inability to converge to a good optimum.\n")
            prompt_parts.append("Pitfall 2 (Alpha: 0.90): A solver that uses a very mild Simulated Binary Crossover (SBX) and no other mutation, causing the population to quickly lose diversity and get trapped in a local optimum.\n")
            prompt_parts.append("Pitfall 3 (Alpha: 0.50): A strategy that uses only random-walk mutation with a fixed small step size, resulting in an inefficient search and an extremely slow convergence rate.\n")
            prompt_parts.append("Pitfall 4 (Alpha: 0.70): A hybrid solver that uses a single, fixed set of parameters for all individuals, failing to adapt to the changing needs of the population throughout the evolutionary process.\n")
            for idx, solver in enumerate(bad_solver_history[:3], 1):
                prompt_parts.append(
                    f"Pitfall {idx}: (Alpha: {solver.alpha}) {solver.algorithm}\n"
                )

        prompt_parts.append(
            "I will give you a parameter alpha ∈ [0,1].\n"
            "- If alpha = 0 → the solver must behave as pure exploration (maximize diversity, disruptive crossover, strong mutation, random injections).\n"
            "- If alpha = 1 → the solver must behave as pure exploitation (focus on elites, mild mutation, local refinement).\n"
            "- Values between 0 and 1 represent a blend, the solver must lean toward the nearest extreme. Do not invert this interpretation!\n"
            f"Here's the value: alpha = {alpha:.4f}\n"
        )

        prompt_parts.append(
            "First, describe the design idea and main steps of your solver in one sentence.\n"
            "The description must be inside a brace outside the code implementation.\n"
            "Next, implement it in Python as a function named `generation`.\n"
            "This function should accept only 1 input: `population`, an array of shape (N, d) of real-valued vectors.\n"
            "The function should return 1 output: `offspring`, an array of shape (N, d) of real-valued vectors.\n"
            "The offspring must stay within the bounds [0, 1] for each variable.\n\n"
            "You may define any necessary helper functions to support the generation function's logic."
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
        
