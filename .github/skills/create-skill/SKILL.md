---
name: create-skill
description: "Guide the authoring of a reusable VS Code skill file (SKILL.md) for this repository."
argument-hint: "Describe the workflow, checklist, or outcome the new skill should capture."
---

This skill helps you create a workspace-scoped `SKILL.md` that captures a repeatable workflow, decision process, or multi-step methodology.

Use this skill when you want to turn a conversation, review process, or task pattern into a reusable skill for the repo.

Steps:
1. Clarify the outcome.
   - What should the skill produce?
   - Is the skill repo-scoped or personal?
   - Should it be a short checklist or a full multi-step workflow?

2. Choose the correct location.
   - Workspace-scoped skills belong under `.github/skills/<name>/SKILL.md`.
   - User-scoped skills belong in `{{VSCODE_USER_PROMPTS_FOLDER}}/` if supported.

3. Draft the skill frontmatter.
   - `name`: the skill identifier, matching the folder name.
   - `description`: clear, trigger-friendly explanation of when to use it.
   - `argument-hint`: prompt the user for the desired output.

4. Write the body.
   - Summarize the workflow clearly and concisely.
   - List the step-by-step process, branching logic, and completion criteria.
   - Include quality checks and validation steps.
   - Use plain language so the skill is easy to follow.

5. Validate the skill.
   - Confirm the file is in the correct path.
   - Verify the YAML frontmatter is syntactically valid.
   - Make sure the description and instructions are actionable.

If the workflow is not yet clear, ask for the desired output and whether the skill should focus on:
- implementation guidance,
- documentation/review checklists,
- debugging or design processes,
- or product/UX decision support.

This skill is intentionally general so it can be reused whenever a repo-specific SKILL.md needs to be created or refined.