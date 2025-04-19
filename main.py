import os
import time
import argparse
from datetime import datetime
from litellm import completion
import litellm
from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import BaseModel
import json
from agents.brd import BRDAgent
from agents.prd import PRDAgent
from agents.user_stories import UserStoriesAgent
from agents.coding_instructions import CodingInstructionsAgent

class DirectoryName(BaseModel):
    directory_name: str

def get_output_dir(prompt: str) -> str:
    now_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response = completion(
        model="openai/gpt-4o-mini",
        messages=[
            {'role': 'developer', 'content': 'You are a helpful assistant that generates a unique short directory name for a project based on the prompt.'},
            {'role': 'user', 'content': prompt},
        ],
        response_format=DirectoryName,
    )
    directory_name = DirectoryName(directory_name=json.loads(response["choices"][0]["message"]["content"])["directory_name"] + "_" + now_string)
    return f"output/{directory_name.directory_name}"

def main(spec_file: str):
    litellm.drop_params=True
    # Get today's date in the format "June 5th, 2025"
    today = datetime.now().strftime("%B %d, %Y")
    with open(spec_file, "r") as f:
        initial_spec = f.read()

    output_dir = get_output_dir(initial_spec)
    os.makedirs(output_dir, exist_ok=True)

    initial_start_time = time.time()
    total_cost = 0

    print("Generating BRD...")
    brd_agent = BRDAgent()
    brd, cost = brd_agent.run({"spec": initial_spec, "today": today}, output_dir)
    total_cost += cost

    print("Generating PRD...")
    prd_agent = PRDAgent()
    prd, cost = prd_agent.run({"brd": brd, "today": today}, output_dir)
    total_cost += cost

    print("Generating User Stories...")
    user_stories_agent = UserStoriesAgent()
    user_stories, cost = user_stories_agent.run({"prd": prd, "today": today}, output_dir)
    total_cost += cost

    print("Generating Coding Agent Instructions...")
    coding_agent = CodingInstructionsAgent()
    _, cost = coding_agent.run({"user_stories": user_stories, "prd": prd}, output_dir)
    total_cost += cost

    print(f"Outputs saved to {output_dir}")
    print(f"Total cost: {total_cost:.2f} USD")
    print(f"Total time: {time.time() - initial_start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=str, default="spec.md", required=False)
    args = parser.parse_args()
    main(args.spec)
