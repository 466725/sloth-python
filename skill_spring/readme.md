# Skill Spring Learning Lab

`skill_spring/` is the repository’s collection of learning exercises,
experiments, and standalone examples. It spans algorithms, Python and test
automation concepts, Claude Code and MCP projects, web scraping, and small
creative programs.

These examples are for study and experimentation. They are not part of the
production stock-analysis application, and application code should not depend
on this package. Run an example or project explicitly when you want to explore
it.

## Learning areas

| Area | Contents | Start here |
| --- | --- | --- |
| [Algorithms](algorithms/) | Implementations and exercises in data structures, sorting, searching, recursion, dynamic programming, backtracking, strings, mathematics, machine learning, and related techniques. | Browse by topic under `algorithms/`; see the [normal-distribution quicksort notes](algorithms/sorts/normal_distribution_quick_sort.md). |
| [Programming and test concepts](concepts/) | Small examples covering Python types, decorators, fixtures, assertions, DDT, CLI and CI/CD, plus browser automation topics such as frames, shadow DOM, contexts, alerts, forms, and file uploads. | Open the example matching the concept, such as [`fixture.py`](concepts/fixture.py), [`browser_context.py`](concepts/browser_context.py), or [`ci_cd.py`](concepts/ci_cd.py). |
| [Claude Code and MCP](claude_code/) | Practice applications, MCP client/server and transport demos, notebook exercises, certification study material, and a Claude Agent SDK project. | Use the [Claude Code learning index](claude_code/claude_code_learning.md) for the project-by-project map. |
| [Web scraping and networking](web_scraping/) | Website scraping examples, screenshot capture, hostname/IP lookup, and TCP client/server samples. | Browse [`web_scraping/`](web_scraping/) and choose the example you want to study. |
| [Small programs and games](fun_part/) | Beginner exercises, text and number utilities, games, a calculator, and an education-management example. | Browse [`fun_part/`](fun_part/) or start with [`calculator.py`](fun_part/calculator/calculator.py). |

## Claude Code and MCP projects

The `claude_code/` area contains several projects, each focused on a different
part of Claude Code or MCP. Many have their own `README.md`, `pyproject.toml`,
and `uv.lock`; follow the instructions in the individual project instead of
assuming that the repository-wide Python environment applies.

| Project | Focus |
| --- | --- |
| [`001_starter`](claude_code/001_starter/README.md) | Introductory MCP server exposing document and math tools. |
| [`002_cli`](claude_code/002_cli/README.md) | CLI chat application with MCP tools and document retrieval. |
| [`003_notifications`](claude_code/003_notifications/README.md) | MCP stdio notifications and progress updates. |
| [`004_roots`](claude_code/004_roots/README.md) | Chat demo with MCP roots and controlled filesystem access. |
| [`005_sampling`](claude_code/005_sampling/README.md) | MCP sampling, logging, and progress flow. |
| [`006_transport_http`](claude_code/006_transport_http/README.md) | MCP interaction using HTTP transport. |
| [`007_note_book`](claude_code/claude_code_learning.md) | Notebook exercises on prompting, tools, evaluation, retrieval, embeddings, images, and related topics. |
| [`claude_agent_sdk`](claude_code/claude_agent_sdk/README.md) | SDK source, examples, tests, and release material. |
| [Architect Foundations practice exam](claude_code/000_Architect_Foundations_Certification_Exam/README.md) | Community-created practice questions and an interactive Claude Code skill. |

## How to use the examples

- Start in the relevant directory and read its `README.md` when present.
- For a standalone Python example, inspect its imports and any comments or
  configuration before running it. Some examples contact external websites or
  services, so their behavior depends on network access and the remote service.
- For a Claude Code or MCP subproject, use its own environment and setup
  instructions. Several projects use `uv`; API-based examples may also need
  provider credentials.
- Some Python examples are meant to be read or adapted rather than run as a
  unified application. There is no single command that launches all of
  `skill_spring/`.
- The repository’s root pytest configuration excludes `skill_spring/` from
  normal test discovery. Projects with their own tests, such as
  [`claude_agent_sdk`](claude_code/claude_agent_sdk/README.md), should be
  validated using that project’s instructions.

## Package boundary

- Production application code does not import or rely on `skill_spring/`.
- Examples here do not participate in stock analysis, the Web/API service,
  notifications, application startup, or deployment.
- Keep experiments self-contained; move generally useful production behavior
  into the appropriate application package before other project code depends
  on it.
