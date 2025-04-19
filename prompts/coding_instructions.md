Create a very very very detailed list of all of the epics and stories for this project plan, with one-story-point tasks that break down each story. It is critically important that all of the details to implement this are in this list.

Note that a very competent AI Coding Agent will be using this list to autonomously create this application, so be sure not to miss any details whatsoever, no matter how much time and thinking you must do to complete this very challenging but critically important task.

Guidelines:
1. Each task should be atomic and focused on a single responsibility
2. Order tasks logically - consider dependencies and implementation sequence
3. Early tasks should focus on setup, core functionality first, then advanced features
4. Include clear validation/testing approach for each task
5. Set appropriate dependency IDs (a task can only depend on tasks with lower IDs)
6. Assign priority (high/medium/low) based on criticality and dependency order
7. Include detailed implementation guidance in the "coding_instructions" field
8. If the PRD contains specific requirements for libraries, database schemas, frameworks, tech stacks, or any other implementation details, STRICTLY ADHERE to these requirements in your task breakdown and do not discard them under any circumstance
9. Focus on filling in any gaps left by the PRD or areas that aren't fully specified, while preserving all explicit requirements
10. Always aim to provide the most direct path to implementation, avoiding over-engineering or roundabout approaches
11. The status of each task should be 'Pending'

<project-plan>
{{ prd }}
</project-plan>

<user-stories>
{{ user_stories }}
</user-stories>

**Final note**: If you are suggesting altering database structures, migrations, etc - make sure you are not introducing inconsistancies between foreign keys, pivot tables, etc.  If a new foreign key needs added to an existing table/model - make sure it is a new migration or action, not a modification to an existing one.
