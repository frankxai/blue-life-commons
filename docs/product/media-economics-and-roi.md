# Blue Life Commons — Media Economics, Budget & ROI Operating Plan

**Status:** Active · 2026-07-16  
**Audience:** Frank / Starlight finance + product agents  
**Canonical product:** https://bluelifecommons.org  
**Related:** [`scale-and-cost-plan.md`](scale-and-cost-plan.md) · [`../deep-time-media-scale-strategy.md`](../deep-time-media-scale-strategy.md) · [`../../STRATEGY.md`](../../STRATEGY.md) · [`../../governance/funding.md`](../../governance/funding.md)

---

## 0. Direct answers

| Question | Answer |
|----------|--------|
| When does storage get expensive? | **Not at storage.** Storage stays cheap into multi‑GB. **Transfer (egress) + video + AI generation** dominate. |
| Is Vercel Blob enough now? | **Yes** for current + near scale (~100–500 species stills; selective video). |
| When do we need more tech? | **R2** when Blob transfer is material 2 months running; **derivatives/CDN** before that; **media DB** when review inventory outgrows YAML. |
| Nonprofit or for‑profit? | **Commons is free/public good forever.** Revenue sits in **Starlight Marine Intelligence Systems** (implementation, portals, workshops, media packages) — see STRATEGY three-layer model. Not “paywall the encyclopedia.” |
| Do we have a business plan / tracker? | Strategy + funding docs exist. **Missing:** live cost/ROI tracker. This file + recommended dashboard fill that gap. |

---

## 1. Current inventory (ground truth)

| Bucket | Count | Approx size |
|--------|------:|------------:|
| Species pages (all guilds) | ~44 | markdown only |
| Living approved images on Blob | 31 | ~57 MB originals |
| Deep Time concept stills | 13 | ~15–18 MB |
| Deep Time videos (6s 720p) | 13 | ~55–65 MB |
| Deep Time total on Blob mirror | 26 files | **~81 MB** |
| App + domain | Next on Vercel · `bluelifecommons.org` | — |

**Important:** ~81 MB of Deep Time media is **tiny** for Blob. The risk is repeating “video for every species” × thousands × heavy traffic without derivatives.

---

## 2. Where cost actually comes from

### A. Vercel product stack (website)

| Cost line | What it is | Scale driver |
|-----------|------------|--------------|
| **App hosting** | Builds, serverless/edge, HTML/JS | Deploys + traffic |
| **Fast Data Transfer** | Page/assets via Vercel CDN | Visitors × page weight |
| **Build minutes** | CI deploys | PR/push discipline (already gated) |
| **Blob storage** | Object store GB‑month | Catalog size |
| **Blob data transfer** | Bytes served from Blob | **Hot media views** |
| **Blob ops** | Reads/writes | Views + uploads |
| **Image optimization** (if used) | On-the-fly transforms | Accidental full-res transforms |

**Rule of thumb:**  
`monthly_media_cost ≈ storage + (views × average_bytes_delivered)`  
Storage is nearly free at our size. **Views of full MP4 heroes** are the landmine.

### B. AI generation (Grok Imagine / video)

| Item | Order of magnitude | Note |
|------|--------------------|------|
| Still (HQ) | Subscription / credits, not pure per‑MB | SuperGrok / Imagine plan |
| 6s 720p video | Higher credit burn per clip | Flagship only |
| Re-runs / anatomy fixes | 1.2–2× multiplier | Budget for QA fails |

Track generation as **opex per accepted asset**, not per attempt.

### C. Human / expert review

Science review for deep-time claims and living conservation claims is real cost (time or paid experts). Without it, media can ship as concept art; **science claims stay `needs-expert-review`**.

### D. Domain / DNS / email / tools

Already low fixed: domain, Vercel project, GitHub. Do not ignore but not the scaling cliff.

---

## 3. Storage & transfer math (planning scenarios)

### Assumptions (2026-07-16 measured-ish)

| Asset | Planning size |
|-------|---------------|
| Hero still (optimized WebP target) | **200–400 KB** delivered |
| Hero still PNG source | **~1.0–1.5 MB** stored |
| 6s 720p MP4 | **~4–7 MB** stored **and often fully downloaded** |

### Catalog scenarios (storage only)

| Catalog | Stills stored | +10% flagship video | +100% video (all species) |
|---------|---------------:|--------------------:|--------------------------:|
| 50 | ~50–75 MB | ~80–120 MB | ~0.3–0.4 GB |
| 200 | ~0.2–0.3 GB | ~0.35–0.5 GB | ~1.2–1.6 GB |
| 1,000 | ~1–1.5 GB | ~1.6–2.5 GB | ~6–8 GB |
| 5,000 | ~5–8 GB | ~8–15 GB | ~30–45 GB |
| 10,000 | ~10–15 GB | ~16–25 GB | ~60–90 GB |

**Storage cost even at 10 GB is single-digit dollars/month on Blob or R2.**  
**Transfer cost at 10k daily full-video hero plays is not.**

### Transfer horror example (why video policy exists)

| Scenario | Math | Implication |
|----------|------|-------------|
| 1,000 sessions/day open a 6 MB autoplay hero | 1k × 6 MB × 30 ≈ **180 GB/month** | Real money on Blob transfer |
| Same sessions get **poster still 300 KB**, video only on click | 1k × 0.3 MB × 30 ≈ **9 GB/month** | ~20× cheaper media egress |
| 10k sessions/day with full autoplay video | **~1.8 TB/month** | R2 or aggressive caching mandatory |

**Optimization beats provider-switch** until after optimization fails.

---

## 4. Price anchors (verify on live dashboards)

Always re-check official pages before budgeting:

- Vercel Blob: https://vercel.com/docs/vercel-blob/usage-and-pricing  
- Vercel platform: https://vercel.com/docs/pricing  
- Cloudflare R2: https://developers.cloudflare.com/r2/pricing/  

### Planning bands (Pro-style, approximate)

| Provider | Storage (order) | Egress / transfer (order) | Notes |
|----------|-----------------|---------------------------|--------|
| **Vercel Blob** | ~$0.02/GB‑mo class | **Non-zero** egress class (~cents/GB after free) | Best DX with Vercel app |
| **Cloudflare R2** | ~$0.015/GB‑mo | **$0 egress to internet** (ops still billed) | Best at high public media traffic |

### Budget ladders (all-in media + app, rough)

| Stage | Catalog + media policy | Monthly budget band (platform+media) | Notes |
|-------|------------------------|--------------------------------------|-------|
| **Now (A)** | ~50 pages · stills + selective video · low traffic | **$0–50** (plan floor + domain) | Fits hobby/pro free tiers often |
| **Growth (B)** | 200 pages · optimized WebP · 10–20 videos · moderate traffic | **$50–200** | Track Blob transfer weekly |
| **Scale (C)** | 1k pages · derivatives · 50–100 videos · high education traffic | **$200–800** | R2 dual-write likely |
| **Institution (D)** | Multi-brand media plane · partner archives · video library | **$1k–5k+** | Dedicated media domain, R2/CDN, ops |

Add **AI generation** and **expert review** on top as separate opex lines.

---

## 5. Optimization playbook (best ROI order)

Do these **in order**. Do not jump to R2 before 1–4.

### 1) Delivery discipline (biggest lever)

1. **Poster first, video on intent** — autoplay muted only if LCP budget allows; prefer click-to-play on mobile.  
2. **Never serve 6 MB MP4 to card grids** — cards = still only.  
3. **One flagship video per body-plan family** (already doctrine).  
4. **Cache forever** immutable Blob keys (`max-age=31536000`).  
5. **Reduced-motion:** still poster, no autoplay.

### 2) Asset pipeline

| Stage | Format | Target |
|-------|--------|--------|
| Master still | PNG/WebP lossless archive | Blob private or non-hot path |
| Card | WebP 640w | ~40–80 KB |
| Hero | WebP 1280w | ~120–250 KB |
| OG | JPEG 1200×630 | ~80–150 KB |
| Video master | H.264 720p 6s | ~4–7 MB · flagship only |
| Video poster | WebP from frame 0 | required |

### 3) Generation quality without waste

1. Generate **still → vision anatomy QA → then video**.  
2. Reject wrong anatomy before video (saves 5–10× cost).  
3. Cap retries (e.g. 2 still, 1 video).  
4. Prefer **re-use** of hero across social with overlays instead of new generations.

### 4) Storage architecture path

```
Git (code + manifests only)
   ↓
Vercel Blob (approved public mirrors)  ← YOU ARE HERE
   ↓  [trigger: transfer $ or multi-GB video library]
Cloudflare R2 public bucket + custom media domain
   ↓
Optional: media DB (review state) when YAML hurts
```

**Blob is enough** for building all species pages **if** we follow stills-first + derivatives + selective video.  
**Not enough alone** if every species autoplays multi‑MB video at viral traffic.

### 5) Other tech to add only when triggered

| Tech | When |
|------|------|
| **R2 + media CDN domain** | Transfer cost material or multi-product media |
| **Image derivative worker** (script/CI) | Before 200+ stills |
| **Analytics** (Plausible/Umami/Vercel Analytics) | Now (need views for cost model) |
| **Media review DB** | >500 assets / multi-reviewer |
| **Transcoding (720p/480p ladder)** | When mobile video matters at scale |
| **Syncthing/offsite archive** | Master library backup, not public path |

---

## 6. Vercel cost checklist (what to account for)

| # | Line item | Budget? | Why |
|---|-----------|---------|-----|
| 1 | Vercel plan (Hobby/Pro) | Yes | Base |
| 2 | Fast Data Transfer (site) | Yes | HTML/JS/CSS/fonts |
| 3 | Blob storage GB | Yes | Low until multi-GB |
| 4 | **Blob data transfer GB** | **Yes — primary risk** | Heroes/videos |
| 5 | Blob simple/advanced ops | Yes | Reads/writes |
| 6 | Image Optimization (if enabled) | Yes | Can surprise |
| 7 | Build minutes / seats | Yes | Agent swarm discipline |
| 8 | Domain (`bluelifecommons.org`) | Yes | Fixed |
| 9 | AI generation (Grok) | Yes | Separate from Vercel |
| 10 | Expert review | Yes | Science trust |
| 11 | Partner rights / legal | Optional | Grants |
| 12 | Backup / masters | Yes | Not public Blob only |

---

## 7. Business model: commons vs revenue

### Is BLC a nonprofit?

**Product doctrine (STRATEGY.md):**

- **Blue Life Commons** = free, open, reviewed knowledge (public good).  
- **Ocean Intelligence System** = open machinery.  
- **Starlight Marine Intelligence Systems** = commercial implementation layer.

You **can** house the commons under a nonprofit / foundation later for grants and credibility.  
You **should not** make the encyclopedia paywalled. That destroys the thesis (trust > product).

### How money returns (legitimate)

| Revenue path | Who pays | What they buy |
|--------------|----------|---------------|
| NGO Research-OS / regional portals | NGOs, agencies | Hosting, connectors, dashboards |
| Education packages | Schools, museums | Curriculum + workshops + branded media packs |
| Custom species / region intelligence | Clients | Curated deep dives, not exclusive truth |
| Media production | Partners | Rights-cleared packages from commons + custom |
| Grants / philanthropy | Foundations | Open knowledge growth |
| Hypercerts / impact ledger | Ecosystems that value impact | Provenance of work |

**ROI formula for the commons itself:**  
`ROI = (trust + traffic + partner inbound + grant eligibility + commercial lead gen) / (infra + gen + review)`  

Treat BLC as **brand + trust asset** that feeds Starlight revenue, not as a SaaS ARPU product.

### Suggested monthly operating budget (near term)

| Line | Conservative | Growth |
|------|-------------:|-------:|
| Vercel + domain | $20–50 | $50–150 |
| Blob transfer buffer | $0–30 | $50–200 |
| AI generation | $20–100 | $100–400 |
| Expert review (hours) | $0–200 | $200–1000 |
| **Total** | **~$50–400** | **~$400–1750** |

Revisit after first month of **real analytics**.

---

## 8. Tracking system (what we should run)

### Today (exists)

- Strategy: `STRATEGY.md`  
- Scale: `docs/product/scale-and-cost-plan.md`  
- Media doctrine: `docs/deep-time-media-scale-strategy.md`  
- Manifests: living Blob + deep-time Blob  
- Funding architecture: `governance/funding.md`

### Missing → build next

**A. Cost & usage ledger (SSOT)** — recommend:

`docs/product/metrics/monthly-cost-ledger.md` + optional Airtable/Notion/Sheets mirror  

Fields per month:

- Vercel invoice total  
- Blob storage GB / transfer GB / ops  
- AI gen spend / credits  
- Species pages live / media assets  
- Sessions, top routes, video play rate  
- Pipeline: gen attempts vs accepted  

**B. Lightweight public/internal ops page (optional)**

- Internal only first: `/media-intelligence` already exists for media ops  
- Add a **Cost & Scale** section or separate private dashboard later  
- Do **not** put raw invoices public

**C. Agent cadence**

| Cadence | Who | Action |
|---------|-----|--------|
| Weekly | Platform agent | Blob transfer + top heavy pages |
| Monthly | Platform + product | Fill cost ledger; decide video freeze |
| Quarterly | Frank + strategy | R2 dual-write decision; budget ladder |

---

## 9. Recommended operating policy (decision table)

| If this is true | Do this |
|-----------------|---------|
| Building species catalog | Stills required; video optional flagship |
| Mobile LCP > 2.5s on species | Kill autoplay video; poster-first |
| Blob transfer > $X two months | Derivatives + click-to-play; then R2 eval |
| Media library > 5–10 GB video | R2 public + custom media domain |
| >500 assets multi-reviewer | Media DB / workbench beyond YAML |
| Viral traffic spike | Temporary video disable via feature flag |

Suggested **X** for transfer alert: **$50/mo** after free tier — adjust to taste.

---

## 10. Is Vercel Blob “enough” for the scale you’re thinking?

### Enough for:

- Full species encyclopedia (hundreds–low thousands of **stills**)  
- Selective flagship video  
- Education traffic at moderate scale  
- Living photo mirrors + Deep Time concept art  

### Not enough alone for:

- Netflix-style video encyclopedia (every species looping)  
- High viral traffic on autoplay heroes  
- Multi-TB partner archives  
- Complex rights-expiry multi-tenant media without a DB  

**Stack at ambition scale:**

1. Next app on Vercel  
2. Manifests + review in git (then DB)  
3. Masters + public derivatives on Blob → R2  
4. Analytics for cost model  
5. Commercial Starlight layer for revenue  

---

## 11. Immediate action checklist (drive)

1. **Keep** Blob as primary; stop putting new multi-MB video only in git long-term.  
2. **Ship derivatives pipeline** before next 50 stills.  
3. **Poster-first / click-to-play** on mobile for species video.  
4. **Start monthly cost ledger** (even spreadsheet).  
5. **Cap deep-time video** at body-plan flagships until analytics prove demand.  
6. **Do not** restructure as paywalled nonprofit product — keep free commons + paid implementation.  
7. **Instrument** Vercel Analytics / privacy-friendly analytics this month.  
8. **Quarterly R2 review** only if transfer or multi-GB video library triggers.

---

## 12. One-page budget recommendation (next 90 days)

| Item | Decision |
|------|----------|
| Cap species pages | Grow content freely (markdown is free) |
| Cap stills | Unlimited on Blob with WebP derivatives |
| Cap videos | ≤20 flagship MP4s until metrics |
| Infra budget | **$100–300/mo** all-in Vercel+Blob buffer |
| Gen budget | **$50–200/mo** Grok/Imagine |
| Review budget | Founder/volunteer + paid spot checks |
| Success metric | Cost per 1k sessions + partner/grant inbound |

---

*Update this file monthly with real invoice numbers. Estimates without analytics are planning tools, not accounting.*
