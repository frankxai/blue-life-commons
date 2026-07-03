# Grok Image Generation Handoff

Use this handoff when Codex, Grok, or Antigravity generates the visual library.

## Output Directory

```text
C:\Users\frank\starlight\repos\_generated\media\blue-life-commons\2026-06-26-visual-system\
```

Approved files can later be copied into this repo under `assets/generated/` with their metadata.

## Headless Command

```powershell
$env:HOME=$env:USERPROFILE
$prompt = Get-Content -Raw -LiteralPath "C:\Users\frank\starlight\repos\blue-life-commons\docs\visual-system\grok-batch-001-prompt.md"
grok -p $prompt --no-alt-screen --always-approve --max-turns 20 --output-format plain
```

## Constraints

- Use Grok Imagine image generation only for non-factual scene imagery.
- Do not render exact labels, UI text, captions, charts, maps, or claims inside the pixels.
- Avoid unsafe proximity to wildlife, feeding, touching, chasing, baiting, crowding, or glamorized captivity.
- Keep animals in respectful, plausible habitat scenes.
- Save local files and return absolute paths.
- Write a `media-job.json` next to outputs.
- Include the prompt ID in each file name.
- Grok supported aspect ratios observed in this batch: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`, `2:3`, `3:2`, `9:19.5`, `19.5:9`, `9:20`, `20:9`.
- For scenes with notebooks, forms, cards, laptops, or posters, say: "blank surfaces, no writing, no pseudo-text, no scribbles, no fake interface glyphs."

## Batch Strategy

Run in batches of 6 to 12 images, not all 40 at once.

1. Generate batch.
2. Inspect exports.
3. Score each output.
4. Tighten prompts.
5. Generate the next batch.

## QA Note Template

```text
<prompt_id>
Path:
First read:
Animal safety:
Crop:
Artifacts:
Use:
Score:
Decision:
```

## Antigravity/Codex Prompt

```text
Run the full Agentic Design Loop for Blue Life Commons visual assets.
Read docs/visual-system/brand-pack.md, docs/visual-system/grok-prompt-matrix.json, ETHICS.md, SOURCES.md, STYLE.md, and WELFARE.md.
Use Grok Imagine for source images only.
Do not render factual text or labels inside images.
Save outputs under C:\Users\frank\starlight\repos\_generated\media\blue-life-commons\2026-06-26-visual-system\.
Return absolute output paths, prompt IDs, tool calls used, and QA notes.
```
