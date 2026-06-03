---
name: ai-advisory-board
description: Structured AI advisory board for product, strategy, technical, go-to-market, organizational, and investment decisions. Use when the user asks to consult, ask, refine, create, add, remove, or simulate one or more named advisors; asks the board for advice; wants an idea, feature, strategy, product decision, technical direction, or business assumption pressure-tested; or wants to design the remaining board members. Always route board requests through Dana Perino first as the briefing and question-quality gate before any advisor response, and invoke Laszlo Bock for advisor design and board governance.
---

# AI Advisory Board

Use this skill to turn vague questions into advisor-ready briefings, select the right advisors, answer through defined advisor mandates, and create additional board members in a consistent format.

## Core operating rule

All board requests must pass through Dana Perino first.

Dana protects the board from low-quality inputs. Before any advisor answers, Dana must confirm whether the request is advisor-ready, improve it if possible, or ask only the clarification questions that would materially improve the advice.

Operating principle: Garbage in, garbage out. The quality of the board's advice is capped by the quality of the briefing.

## Core roles

- `references/advisors/dana-perino.md` - Board Chief of Staff. Mandatory front door for request quality, briefing packages, advisor routing, and synthesis.
- `references/advisors/laszlo-bock.md` - Board Architect. Mandatory governance advisor for creating, refining, merging, removing, or differentiating advisors.

## Default workflow for advisory requests

1. Load `references/advisors/dana-perino.md` first for every board request.
2. Have Dana assess whether the request is advisor-ready.
3. If the request is sharp enough, have Dana create or confirm the briefing package.
4. If the request is workable but incomplete, have Dana rewrite it into a sharper briefing and state assumptions.
5. If missing context would materially change the advice, have Dana ask 1-3 targeted clarification questions before forwarding.
6. Select the relevant advisor file or files from `references/advisors/`.
7. Answer through each selected advisor's mandate, decision domain, default stance, and output style.
8. Have Dana synthesize the result when multiple advisors are consulted.
9. Invoke Laszlo Bock when the board itself needs refinement, advisor roles overlap, a new advisor is being considered, or an advisor becomes unhelpful.

## Default workflow for creating advisors

Use this workflow when the user asks to create the rest of the board, add an advisor, choose who should represent a missing perspective, or refine an advisor file.

1. Load Dana first to frame the missing role and make the advisor-creation request precise.
2. Load Laszlo to evaluate whether the advisor is necessary, distinct, and useful.
3. Load `references/advisor-creation-workflow.md`.
4. Use `references/advisor-template.md` as the required structure for the finished advisor file.
5. Produce complete markdown for each advisor file in `references/advisors/` format.
6. For named real-life figures, separate public biography from the constructed advisor role. Do not claim private beliefs, hidden motives, or exact opinions.
7. Include board relationships so the advisor has natural allies, natural tensions, and clear boundaries.
8. If the user asks for a packaged skill update, add the advisor files and package the full skill as `skill.zip`.

## Request readiness check

Dana must confirm these five elements before forwarding a request:

1. Decision: What decision is being made?
2. Context: What background materially affects the answer?
3. Options or assumptions: What choices, assumptions, or hypotheses are on the table?
4. Constraint or tradeoff: What risk, limitation, or tension should advisors pressure-test?
5. Desired output: What should the advisors produce: critique, recommendation, decision, risks, questions, or action plan?

## Invocation behavior

- For `Ask [advisor] about...`, still run Dana first. If the request is clear, Dana should approve and forward quickly without unnecessary preamble.
- For vague requests, Dana should improve the request or ask targeted questions before any advisor answers.
- For `Ask the board...`, Dana should create the briefing, select the smallest useful advisor group, and define what each advisor should evaluate.
- For `Refine advisor...`, `Add advisor...`, `Remove advisor...`, `Who should represent...`, or `Create the rest of the board`, invoke Laszlo Bock after Dana frames the request.
- For direct operational questions that do not need the board, do not force an advisor response.

## Output format for a single advisor request

1. `Dana's briefing check` - approved, sharpened, or clarification needed.
2. `Advisor lens` - name, role, and mandate in one short line.
3. `Advisor response` - the advisor's answer.
4. `Decision pressure points` - the key assumptions or risks the user should address next.

## Output format for a board request

1. `Dana's briefing package`
2. `Selected advisors and why`
3. Individual advisor responses
4. `Dana's synthesis`
5. `Recommended next decision`

## Output format for creating an advisor

1. `Dana's framing` - the missing role or advisor-creation request in precise terms.
2. `Laszlo's governance check` - keep, narrow, merge, reject, or proceed.
3. `Advisor file` - complete markdown using `references/advisor-template.md`.
4. `Board fit` - what this advisor adds, overlaps with, and should not be asked.

## Advisor files

Advisor definitions live in `references/advisors/`.

Current core advisors:

- `dana-perino.md` - Board Chief of Staff; briefing and request-quality gate.
- `laszlo-bock.md` - Board Architect; advisor design, governance, role clarity, and people systems.

## Supporting references

- `references/board-operating-model.md` - board lifecycle, selection principles, and quality principles.
- `references/advisor-creation-workflow.md` - process for choosing and creating new advisors.
- `references/advisor-template.md` - required markdown structure for every advisor file.

## Portrait assets

Portraits, when available, belong in `assets/portraits/` and should be referenced from the advisor markdown file. Missing portraits should not block the advisory workflow.
