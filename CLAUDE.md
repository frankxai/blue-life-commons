# blue-life-commons — Claude Code operating contract

## Web design gate — load-bearing

**Website / web-design work goes through the `web-release-gate` skill first**, before writing UI code. It is the entry point of the `web-excellence` pack in `.claude/skills/` (installed from [`frankxai/claude-skills-library`](https://github.com/frankxai/claude-skills-library) `packs/web-excellence`; re-run its `install.sh` to upgrade). The gate sequences `web-design-guidelines` (live Vercel Web Interface Guidelines audit), `ui-ux-pro-max`, `emil-design-eng` / `apple-design` / `review-animations` for motion, `core-web-vitals`, and `visual-proof`, and defines what "done" requires: audit findings plus before/after screenshots at 375 / 768 / 1440, never a self-assigned score.

Three committed hooks in `.claude/hooks/` make this the default rather than a suggestion — a `SessionStart` note, a `PreToolUse` reminder on the first UI-file edit, and a `Stop` check that blocks once if UI changed with no audit. Between sessions, `.github/workflows/web-excellence.yml` runs the mechanical subset on every PR that touches a UI file, as a ratchet on newly added lines only. Any `design.md` / `taste.md` (or `DESIGN.md` / `TASTE.md`) in this repo outranks every skill in the pack.
