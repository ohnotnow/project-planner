from pydantic import BaseModel
from litellm import completion
from jinja2 import Environment, PackageLoader, select_autoescape
import time

class BaseAgent():
    name="base_agent"
    model="openai/o4-mini"
    reasoning_effort="low"

    def run(self, template_variables: dict, output_dir: str) -> tuple[str, float]:
        start_time = time.time()
        prompt = self.get_prompt(f"{self.name}.md", template_variables)
        output, cost = self.get_completion(prompt)
        end_time = time.time()
        self.write_output(f"{output_dir}/{self.name}.md", output, cost, end_time - start_time)
        return output, cost

    def get_completion(self, prompt: str) -> tuple[str, float]:
        response = completion(
            model=self.model,
            messages=[
                {'role': 'developer', 'content': 'Formatting re-enabled'},
                {'role': 'user', 'content': prompt},
            ],
            reasoning_effort=self.reasoning_effort,
        )
        return response["choices"][0]["message"]["content"], response._hidden_params["response_cost"]

    def get_prompt(self, filename: str, prompt_variables: dict) -> str:
        env = Environment(
            loader=PackageLoader("main", package_path="prompts"),
            autoescape=select_autoescape()
        )
        template = env.get_template(filename)
        return template.render(**prompt_variables)

    def write_output(self, filename: str, content: str, cost: float, time: float):
        with open(filename, "w") as f:
            f.write(content)
            f.write(f"\n\nCost: {cost}")
            f.write(f"\n\nTime: {time}")
