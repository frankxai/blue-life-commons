# Production Proof Page Spec

## Outcome contract

- Audience: curious public, educators, citizen scientists, researchers, conservation organizations, and reuse-oriented developers.
- Surface: Blue Life Commons home first viewport.
- First read: an open ocean-life commons whose records expose sources, rights, review state, and Git history.
- Primary action: explore species records.
- Secondary action: contribute with sources.
- Proof object: the existing whale shark record and approved CC0 primary image.

## Proof fields

- Repository record: `content/species/sharks-rays/whale-shark.md`.
- Three cited authorities: IUCN update, IUCN Red List, and CITES appendices.
- Science/ethics review: required; editor review pending.
- Media: approved CC0 Wikimedia image by cotterillmike.
- Media review: 9/9 checks; promotion allowed.
- Content reuse: CC BY 4.0 with attribution.
- Review detail: science required, ethics required, editor pending.
- Git history: link to the record's commit history, not only the current file.

## Public-good outcome contract

- Repository counts are outputs, not claimed ecological outcomes.
- `/impact` publishes a claim only when its artifact status is `approved` or `published`.
- Pending claims remain measurable as review-queue work and are not promoted as verified impact.
- Hypercert eligibility metadata is not proof of issuance, funding, or real-world impact.

## Responsive contract

Desktop uses an editorial proposition beside the record. Mobile reads proposition → actions → commons counts → record image → provenance trace. License and source links remain visible without hover.

## Performance contract

One approved remote responsive image through `next/image`; no new font, client runtime, motion package, video, canvas, WebGL, or generated asset.

Only the approved Vercel Blob host and Wikimedia `Special:FilePath` fallback are permitted through `next/image`.
