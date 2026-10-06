# Repository Claude Skills

本目录存放仓库级协作 skills，属于版本库资产。

- 规则真源与 Claude 入口：仓库根目录 `CLAUDE.md`（包含实际协作说明的普通 Markdown 文件，不是软链接）
- 本目录中的 skill 需要与 `CLAUDE.md` 保持一致
- `.claude/reviews/` 属于本地分析产物，不作为规则真源

如果未来需要兼容其他 agent 目录（如 `.agents/skills/` 或 `.github/skills/`），应先明确单一真源，再通过脚本或镜像同步，而不是手工长期维护多份同义内容。
