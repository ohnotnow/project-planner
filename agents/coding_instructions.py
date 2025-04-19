import json
from pydantic import BaseModel
from agents.base import BaseAgent
from typing import List
from litellm import completion
from enum import Enum


class Priority(Enum):
    low = "Low"
    med = "Medium"
    high = "High"

class CodingStep(BaseModel):
    step_id: int
    step_description: str
    step_instruction: str
    status: str
    priority: Priority
    step_dependancies: List[int]

class Steps(BaseModel):
    title: str
    coding_steps: List[CodingStep]

class Epic(BaseModel):
    epic_name: str
    epic_description: str
    steps: List[Steps]

class Epics(BaseModel):
    epics: List[Epic]

    def to_markdown(self) -> str:
        markdown = ""
        for epic in self.epics:
            markdown += f"## {epic.epic_name}\n\n{epic.epic_description}\n\n"
            for step in epic.steps:
                markdown += f"\n### {step.title}\n\n"
                for instruction in step.coding_steps:
                    markdown += f"- [ ] (Task ID: {instruction.step_id}) (Priority: {instruction.priority.value}) {instruction.step_description} \n"
                    if instruction.step_dependancies:
                        markdown += f"  - Task Dependencies: {', '.join(str(dep) for dep in instruction.step_dependancies)}\n"
                    markdown += f"  - {instruction.step_instruction}\n"
        return markdown

class CodingInstructionsAgent(BaseAgent):
    name="coding_instructions"
    reasoning_effort="high"

    def get_completion(self, prompt: str) -> tuple[str, float]:
        response = completion(
            model=self.model,
            messages=[
                {'role': 'user', 'content': prompt},
            ],
            reasoning_effort=self.reasoning_effort,
            response_format=Epics,
        )
        epics = Epics.model_validate_json(response["choices"][0]["message"]["content"])
        formatted_epics = epics.to_markdown()
        return formatted_epics, response._hidden_params["response_cost"]
