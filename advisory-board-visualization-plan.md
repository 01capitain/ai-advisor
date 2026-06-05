# Advisory Board — Visualization Layer: Design Plan

Collected from the `/grill-me` session on 2026-06-05. This is the working spec
for the HTML presentation layer over terminal-conducted board conversations.

---

## 1. Guiding principles

- **The terminal conducts; the HTML presents.** Conversations happen in the
  Claude Code session. The HTML is a re-presentation layer only.
- **Fidelity rule (hard):** the HTML must contain *everything* from the board
  exchange that was visible in the terminal. It is a re-presentation, never a
  summary. Nothing board-related is omitted or hidden behind an interaction.
- **The data model is durable; the renderer is disposable.** As long as the
  source of truth is plain `conversations/*.md`, switching from a static build
  to a live served app later is just swapping the renderer — no data migration.

---

## 2. Three-tier data architecture

```
Tier 0  session JSONL      raw, append-only, durable    ← Claude Code owns it
        ~/.claude/projects/-var-www-experiments-ai-advisor/<session>.jsonl
Tier 1  conversations/*.md structured export             ← model writes on `save`
Tier 2  advisory-board.html self-contained presentation  ← build generates it
```

- **Rendering model: static build-step generator** (chosen over a served app).
  One self-contained HTML (portraits embedded as base64), opens via `file://`,
  no server. Consistent with the existing `build_board_deck.py`.
- **No hooks.** The build is the **last step of the `save` command**, so the
  HTML can never drift from the md (nothing else writes the md).
- **Migration path:** if the project grows, go "live" by pointing a JS `fetch()`
  at the same `conversations/*.md` (or a generated `index.json`) — the tier-1
  data is unchanged.

---

## 3. Conversation file (Tier 1) schema

- **Slicing:** topic-based — **one file per conversation** (a related thread),
  named `YYYY-MM-DD-<slug>.md`. New turns of the same conversation are
  **appended to the existing file**, not split into new files.
- **Multi-turn from the start** (schema + file format). The HTML multi-turn UI
  can stay simple initially, but the data is multi-turn now.

### Front-matter

```yaml
---
title: Breakfast-List (TAP) MVP — pressure-test & value
date: 2026-06-05          # conversation start = date of the FIRST user prompt
advisors_involved: [dana-perino, marty-cagan, mark-cuban, horst-schulze, dj-patil]
session_id: <uuid>        # back-reference to the Tier-0 transcript (provenance)
---
```

No `status` field (would require unreliable manual upkeep; dropped). No
`updated` field.

### Per-turn anatomy (everything visible in terminal)

```
Turn N
├─ user_prompt
├─ dana
│   ├─ calibration         readiness check: approved / sharpened / clarify
│   ├─ initial_response     the framing / briefing
│   └─ advisor_prompt       *** the exact prompt Dana forwarded to advisors ***
├─ advisors[]   → { name, role, response (FULL, verbatim) }
└─ dana_executive_summary   catch-all for EVERYTHING Dana says after the
                            advisors — synthesis + recommended next decision +
                            anything else. One field, no loss.
```

**New requirement on the consult workflow:** Dana must now emit an explicit,
quotable **`advisor_prompt`** block during the board turn, so it exists in the
transcript for extraction. (Skill/Dana update required.)

---

## 4. HTML information architecture

One self-contained file, three top-level sections; **lands on History**.

- **History** — list of past conversations. Each entry shows exactly:
  **title · date of the last user message · number of turns.** Sorted
  newest-first by last-user-message date. Built by **scanning
  `conversations/*.md` front-matter + turns at build time** (no separate
  manifest to keep in sync). Click → Conversation view.
- **Conversation** — the multi-turn anatomy above: user prompt → Dana
  calibration → Dana initial response → advisor prompt → advisor responses →
  Dana executive summary, with turn navigation. (Absorbs the old
  `advisory-board.html` single-view layout.)
- **Advisors** — gallery of **all** advisors, generated from the skill assets.

### Advisor card component (shared by Conversation + Advisors)

Two-face flip card, used identically everywhere:

- **Front:** portrait · **Name** · **Advisor role** · **Position** (real-world
  credential).
- **Back:** **Default stance** · **When to ask** · **Signature questions**.
- The **full advisor response is always-visible prose in the turn body** — never
  on the back of the card, never behind the flip. The flip only ever toggles
  identity ⇄ background.

### Card field mapping (parsed from `references/advisors/*.md`)

| Card element | Source |
|---|---|
| Portrait | `assets/portraits/<slug>.png` |
| Name | `**Real-life figure:**` |
| Advisor role | `**Advisor role:**` |
| Position | new `## Position` section (see §5) |
| Back — stance | `### Default stance` |
| Back — when to ask | `## Use this advisor when` |
| Back — signature questions | `### Signature questions` |

---

## 5. Advisor `.md` rework

Add a dedicated single-line section to all 13 advisor files — the real-world
credential that qualifies the figure as a role model, distinct from the advisor
*role*:

```markdown
## Position

Co-founder and former CEO of Apple; chairman of Pixar.
```

Card front now reads: **Name → Advisor role → Position.**

---

## 6. `assets/advisor-style.json` (explicit theming asset)

Lives in the skill, keyed by slug, shaped to grow (logo, customizations later):

```json
{
  "steve-jobs":  { "accent": "#8B5CF6" },
  "marty-cagan": { "accent": "#0EA5E9" }
}
```

- **Self-healing colors:** if the build detects an advisor with no entry, it
  assigns a real color **deterministically from a curated palette** (indexed by
  slug — stable across rebuilds, no `random()`) and **writes it back** into the
  JSON. Never a neutral fallback. New advisor → entry auto-filled on first
  build; user edits the hex if disliked; never touched again.

---

## 7. Deep links

- `advisory-board.html#/c/<slug>` → opens that conversation.
- `advisory-board.html#/c/<slug>/t/<n>` → opens it scrolled to turn `n`.
- JS reads the fragment on load and on `hashchange`.

---

## 8. The `save` command (single end-to-end action)

Explicit command (e.g. `/ai-advisory-board save`). Steps:

1. Locate the transcript: **newest `*.jsonl`** in the project's
   `~/.claude/projects/…/` dir, **or a specific `<uuid>`** if passed
   (`save <uuid>` — scrape a different/past session). Optional target slug to
   choose which conversation file to append to.
2. Extract the board turns (the model does the judgment — strip harness noise,
   thinking, non-board chatter) into the §3 schema.
3. Write/append `./conversations/<slug>.md`.
4. **Run the build** (last step) → regenerate `./advisory-board.html` from *all*
   conversations + *all* advisor files + `advisor-style.json`.
5. **Print** the manual-open command + deep link to the latest turn. **Do not
   open the browser.**

```
✓ Saved → conversations/2026-06-05-breakfast-list-mvp.md (3 turns)
✓ Built → advisory-board.html
Open:  xdg-open "file:///…/advisory-board.html#/c/2026-06-05-breakfast-list-mvp/t/3"
```

---

## 9. Global skill vs. repo-specific visualization

| Concern | Location | Portable |
|---|---|---|
| Advisor `.md`, portraits, `advisor-style.json`, consult workflow, `build` script, `save` command | the **skill** → promote to **user scope** (`~/.claude/skills/ai-advisory-board/`) | yes — any repo can consult |
| `./conversations/*.md` + generated `./advisory-board.html` | the **current repo** | no |

- Build reads advisors from the (global) skill dir, conversations from the
  **cwd** repo, outputs `./advisory-board.html`.
- **Opt-in marker** = presence of `./conversations/` (or a tiny
  `.advisory-board.json`). Gates both the build target and the wind-down prompt.

### Wind-down reminder

- **Chosen: (B) deterministic `Stop` hook.** A lightweight repo-local `Stop`
  hook prints a reminder ("💡 `/ai-advisory-board save` to persist this
  conversation") when a session ends, **only in opted-in repos** (gated on
  `./conversations/`). Guaranteed and repo-specific. It is a *reminder only* —
  it does not run the build (that stays inside `save`).

---

## 10. Implementation steps

1. Rework 13 advisor `.md` files: add `## Position`.
2. Create `assets/advisor-style.json` with accents for the existing 13
   (port from current build script + `advisor_council_cards.html`).
3. Update `SKILL.md` / Dana workflow: emit explicit `advisor_prompt`; define the
   `save` command; add the repo-gated wind-down instruction; document the §3 md
   schema.
4. Rewrite `build_board_deck.py` → general build:
   - parse advisors (md + portraits + `advisor-style.json`; self-heal colors),
   - parse `conversations/*.md` (front-matter + turns),
   - render the 3-section self-contained HTML (History / Conversation /
     Advisors) with flip cards + deep-link routing.
5. Implement the `save` command logic (transcript parse → md → build → print).
6. Migrate the playground file `conversations/2026-06-05-breakfast-list-mvp.md`
   to the final schema (add `advisor_prompt`; fold "recommended next decision"
   into `dana_executive_summary`; add `session_id`).
7. (Plan/decision) promote the skill to user scope; parameterize build paths
   (`--skill-dir`, `--conversations`, `--out`).

---

## 11. Deferred / future

- **Live served mode** (drop the static build, fetch md/JSON at runtime).
- **User-owned `status`** badge, only if a real "decided/archived" workflow need
  appears.
- **`advisor-style.json` extensions:** per-advisor logo, customizations.
