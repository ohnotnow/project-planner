import json
from pydantic import BaseModel
from agents.base import BaseAgent
from typing import List
from litellm import completion

class CodingInstruction(BaseModel):
    coding_instruction: str

class CodingInstructions(BaseModel):
    title: str
    coding_instructions: List[CodingInstruction]

class Epic(BaseModel):
    epic_name: str
    epic_description: str
    steps: List[CodingInstructions]

class Epics(BaseModel):
    epics: List[Epic]

    def to_markdown(self) -> str:
        markdown = ""
        for epic in self.epics:
            markdown += f"## {epic.epic_name}\n\n{epic.epic_description}\n\n"
            for step in epic.steps:
                markdown += f"### {step.title}\n\n"
                for instruction in step.coding_instructions:
                    markdown += f"- [ ] {instruction.coding_instruction}\n"
        return markdown

class CodingInstructionsAgent(BaseAgent):
    name="coding_instructions"
    reasoning_effort="high"

    def get_completion(self, prompt: str) -> tuple[str, float]:
        response = completion(
            model=self.model,
            messages=[
                {'role': 'developer', 'content': 'Formatting re-enabled'},
                {'role': 'user', 'content': prompt},
            ],
            reasoning_effort=self.reasoning_effort,
            response_format=Epics,
        )
        epics = Epics.model_validate_json(response["choices"][0]["message"]["content"])
        formatted_epics = epics.to_markdown()
        return formatted_epics, response._hidden_params["response_cost"]
