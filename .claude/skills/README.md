# Repository Claude Skills

This directory contains repository-specific Claude skills. The skills provide
repeatable workflows; the shared rules and repository scope remain defined in
[`CLAUDE.md`](../../CLAUDE.md), with detailed development conventions in
[`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Available skills

| Command | Definition | Purpose |
| --- | --- | --- |
| `/analyze-issue <issue_number>` | [`analyze-issue/SKILL.md`](analyze-issue/SKILL.md) | Assess an issue’s evidence, validity, priority, ownership, and recommended handling. Writes an analysis to `.claude/reviews/issues/issue-<number>.md`. |
| `/analyze-pr <pr_number>` | [`analyze-pr/SKILL.md`](analyze-pr/SKILL.md) | Review a pull request’s necessity, description, validation evidence, implementation risks, and merge readiness. Writes a review to `.claude/reviews/prs/pr-<number>.md`. |
| `/fix-issue <issue_number>` | [`fix-issue/SKILL.md`](fix-issue/SKILL.md) | Implement an issue fix after confirming its analysis baseline, then validate and record the change, risks, and rollback guidance. |
| `/cert-exam [question_count]` | [`cert-exam.skill`](cert-exam.skill) | Run an interactive Claude Certified Architect Foundations practice exam, with configurable question count and feedback. |

The issue and pull-request skills are designed to support distinct steps:

1. Use `/analyze-issue` to establish whether an issue is valid and actionable.
2. Use `/fix-issue` to implement an approved, well-scoped issue fix.
3. Use `/analyze-pr` to evaluate a pull request and its evidence before merging.

## Notes

- Follow `CLAUDE.md` and the applicable scoped instructions when a skill’s
  workflow overlaps with repository-wide or package-specific rules.
- Issue and pull-request analysis documents are written under
  `.claude/reviews/`; they are working artifacts, not an alternate source of
  repository policy.
- `cert-exam.skill` expects the question bank at
  `Claude Certification/Claude Certification Exam.md`. That file is not
  currently present at the referenced path, so the practice exam needs its
  question bank added or its source path corrected before it can run.
- Keep this index in sync when skills are added, removed, renamed, or their
  commands and output locations change.
