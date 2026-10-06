# Profile Strategy — Moustafa-Ahmed

This is a working document for the profile landing page (the special
`Moustafa-Ahmed/Moustafa-Ahmed` repository) and the public GitHub profile it
sits behind. It records the audit findings, the prioritized plan, and the
concrete GitHub settings to apply by hand (they live in the web UI, not in this
repository).

---

## 1. Audit findings

### The profile repository (this repo)

**Strengths**
- Correct name, so GitHub renders `README.md` directly on
  [github.com/Moustafa-Ahmed](https://github.com/Moustafa-Ahmed).

**Weaknesses**
- README was 16 lines with no links, no featured work, no contact details, and
  no reason for a visitor to click through to a project.
- No visual identity (no banner, no badges).
- Repository metadata empty: **no description, no topics, no license**.
- No `.gitignore` (nothing to ignore yet, but worth adding if assets appear).

### The wider profile (all 5 public repositories)

| Repository | Language | Notes |
| ---------- | -------- | ----- |
| `warehouse-inventory-engine` | PHP | Strongest project. Deep README, architecture docs, business-rules handbook, Pest suite. |
| `lms` | PHP | Laravel 12 + Livewire + Filament LMS. | 
| `flow` | TypeScript | React + TS "Business Flow Explorer". |
| `Agent-Code-Plan` | HTML | Drop-in Kanban/table planning board. |
| `Moustafa-Ahmed` | — | This profile repo. |

**Cross-cutting weaknesses (all repos):**
- **Every** repository has no description and no topics — the single biggest,
  cheapest win for searchability and first impressions.
- No repository declares a license.
- None set a website/homepage or a demo URL.

**Per-repository issues worth fixing next:**
- `warehouse-inventory-engine`
  - README is framed as a *challenge submission* ("Submission Links", "before
    final submission", "pending owner recording"). For a portfolio, reframe as a
    product/showcase: lead with the problem, the architecture, and a screenshot.
  - Root contains scratch/agent files: `challenge.txt`, `new.txt`,
    `erd.excalidraw`, `boost.json`, `AGENTS.md`, `.agents/`, `.ai/`,
    `.github/skills/`. Keep only what is intentional; move the rest out of the
    public tree.
  - The referenced walkthrough video is still pending.
- `lms`
  - Repository is **~54 MB** — far larger than the source. Almost certainly
    committed dependencies (`node_modules`/`vendor`) or large media. Audit and
    remove from history going forward.
  - README has an "If I Had More Time…" section listing many gaps; trim it to a
    short, confident roadmap instead of a public to-do list.
- `flow`
  - `package.json` `"name": "new"` — rename to `flow` / `business-flow-explorer`.
- `Agent-Code-Plan`
  - Default branch is `master` while every other repo uses `main`; standardize.

---

## 2. Prioritized plan

### Must-do (high impact, do first)
1. **Rewrite the profile README** into a narrative landing page. *(Done on branch
   `showcase/overhaul`.)*
2. **Add a visual header + tech badges.** *(Done.)*
3. **Set a description and topics on every repository** (see §3).
4. **Pin the four projects** in the order below so they appear on the profile.
5. **Add a license** to each real project (MIT unless there is a reason not to).
6. **Shrink `lms`** by removing committed dependencies/media from the working
   tree (and, if acceptable, from history).

### Should-do
7. **Reframe `warehouse-inventory-engine`** from "challenge submission" to
   "showcase project": add a screenshot/GIF at the top, lead with the problem,
   keep the submission links in a collapsed section or remove them.
8. **Clean scratch files** out of `warehouse-inventory-engine` root.
9. **Fix `flow`'s `package.json` name** and add a screenshot to its README.
10. **Add CI** (GitHub Actions: run Pest on push/PR for `lms` and
    `warehouse-inventory-engine`, type-check+build for `flow`).
11. **Expand the GitHub bio** and add a website/social links (see §4).

### Nice-to-have
12. A short demo GIF or recorded walkthrough embedded in the flagship README.
13. A GitHub Pages demo for `flow` / `Agent-Code-Plan` (turns a repo into a
    clickable live demo).
14. A published release/tag on the flagship project.
15. Contribution-activity and streak cards on the profile README (optional —
    they add polish but depend on a third-party service).

---

## 3. Repository metadata to apply

For each repo, **Settings → Description / Topics**, and add a `LICENSE` file.

### `warehouse-inventory-engine`
- **Description:** Inventory reservation engine for a multi-warehouse ERP — correct under concurrent reservations, partial fulfillment, provider timeouts, and duplicate webhooks. Laravel 13 + MySQL.
- **Topics:** `laravel` `php` `mysql` `inventory-management` `erp` `concurrency` `webhooks` `idempotency` `pest` `domain-driven-design`
- **License:** MIT

### `lms`
- **Description:** Mini learning-management system with courses, lessons, enrollment, and progress tracking. Laravel 12 · Livewire 3 · Filament v3 · Pest.
- **Topics:** `laravel` `php` `livewire` `filament` `lms` `e-learning` `pest` `tailwindcss`
- **License:** MIT

### `flow`
- **Description:** Explore a product's business logic as a role-based mind map and interactive flowcharts. React 19 + TypeScript + React Flow.
- **Topics:** `react` `typescript` `react-flow` `visualization` `mind-map` `flowchart` `vite` `json-schema`
- **License:** MIT

### `Agent-Code-Plan`
- **Description:** Drop-in project planning board (table + Kanban) that AI agents update through a single JSON file.
- **Topics:** `kanban` `project-management` `json-schema` `developer-tools` `ai-agents` `vanilla-js`
- **License:** MIT

### `Moustafa-Ahmed` (this profile repo)
- **Description:** GitHub profile — backend engineer building reliable Laravel/PHP systems.
- **Topics:** `profile` `github-profile` `backend` `laravel` `php`

---

## 4. Pinned repositories strategy

GitHub shows up to **6 pinned repositories**. Pin them in this order so the
flagship reads first:

1. **`warehouse-inventory-engine`** — the flagship; deepest engineering signal.
2. **`lms`** — proves full-product, full-stack delivery.
3. **`flow`** — proves frontend/TypeScript range and a different problem type.
4. **`Agent-Code-Plan`** — a small, practical developer tool.
5. *(optional)* `Moustafa-Ahmed` — the profile repo itself.

Do **not** pin forks or empty/scaffold repositories. If a repo has no README,
pin order is irrelevant — a bad repo page hurts more than no pin.

---

## 5. Profile-level settings

- **Bio** (Profile → Edit profile). Suggested:
  > Backend Engineer · Laravel, PHP & MySQL · building reliable, concurrency-safe systems.
- **Website:** add a portfolio, personal site, or LinkedIn URL.
- **Social links / location:** keep Egypt; add LinkedIn if available.
- **Avatar:** a clear, professional headshot or a clean monogram.
- **README contact:** the README currently lists GitHub + email. Add LinkedIn
  (and a personal site) once those URLs exist.

---

## 6. What changed on `showcase/overhaul`

- Rewrote `README.md` into a narrative profile page: pitch, featured projects
  with real descriptions, tech-stack table, engineering highlights, activity,
  and contact.
- Added `assets/header.svg`, a self-contained dark banner (no external
  dependencies, renders on light and dark themes).
- Added this strategy document.

**Not done (requires owner input / web UI):** repository descriptions,
topics, licenses, pinned order, bio, social links, and the cleanup of the other
repositories. Those are settings and cross-repo changes, listed above so they
can be applied deliberately.
