# Content

Versioned knowledge — the source of truth from which public pages are generated.

```
content/
├── species/        # species intelligence pages, by guild
│   ├── cetaceans/      # whales, dolphins, porpoises
│   ├── pinnipeds/      # seals, sea lions, walruses
│   ├── turtles/        # sea turtles
│   ├── sharks-rays/    # sharks, rays, skates
│   └── reefs/          # reef ecosystems and key species
├── regions/        # region ocean briefings
├── research/       # research summaries, dataset cards, notebooks
├── partners/       # partner profiles
├── academy/        # educational lessons
└── events/         # event reports
```

Every artifact carries YAML frontmatter conforming to [schema/artifact-schema.md](../schema/artifact-schema.md) and is validated by CI. See [CONTRIBUTING.md](../CONTRIBUTING.md) for artifact classes and workflow.
