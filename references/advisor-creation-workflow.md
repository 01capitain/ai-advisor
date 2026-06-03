# Advisor Creation Workflow

Use this workflow when the user wants to add, design, or refine board members.

## Goal

Create advisor files that are specific enough to be invoked later with prompts such as:

> Ask Mark Cuban about this feature idea.

The resulting advisor must not be a generic impersonation. It must be a bounded decision lens with a clear mandate, escalation trigger, and failure mode.

## Mandatory sequence

1. **Dana frames the request.**
   - Identify what role or missing perspective the user is trying to add.
   - Confirm the intended decision domain.
   - Clarify whether the advisor should be a named real-life figure, archetype, or internal-style role.

2. **Laszlo evaluates the need.**
   - Decide whether the advisor is functionally necessary.
   - Check overlap with existing advisors.
   - Define what decision this advisor changes that no other advisor would.
   - Reject or merge advisors that are decorative, redundant, or too broad.

3. **Create the advisor definition.**
   - Use `references/advisor-template.md` exactly as the section structure.
   - Include a short bio for named real-life figures.
   - Distinguish the real person from the advisor role.
   - Do not claim private thoughts, exact beliefs, or hidden motives of real people.
   - Use public, high-level career patterns only to define the lens.

4. **Run the quality checks.**
   - Distinctiveness: Does this advisor add a unique lens?
   - Decision impact: Could this advisor change the recommendation?
   - Boundary clarity: Is it clear what they ignore?
   - Tension: Who will they naturally disagree with?
   - Failure mode: How could they become harmful if overused?
   - Invocation clarity: Is it obvious when to call them?

5. **Name and store the file.**
   - Use lowercase kebab-case: `first-last.md` for named figures.
   - Put advisor files in `references/advisors/`.
   - Reference portrait files as `assets/portraits/first-last.png` even if the portrait is not bundled yet.

## Advisor selection rubric

Prefer advisors who cover a missing decision lens, not advisors who are merely admired.

Strong reasons to add an advisor:

- They protect a decision dimension not yet covered.
- They create useful tension with existing advisors.
- They are easy to invoke for a recurring class of questions.
- Their failure mode is understandable and manageable.
- Their advice would be meaningfully different from the rest of the board.

Weak reasons to add an advisor:

- The person is famous or inspiring.
- The person is broadly successful but not tied to a decision domain.
- The role overlaps heavily with an existing advisor.
- The advisor would mostly provide motivational commentary.
- The advisor has no clear escalation trigger.

## Output when proposing a new advisor

When the user asks who should represent a missing position, answer with:

1. Recommended pick
2. Why this pick fits the missing mandate
3. Close alternatives and why they are weaker or different
4. The exact role this advisor would play on the board
5. Draft advisor definition using the advisor template
6. Laszlo's quality check: keep, merge, narrow, or reject

## Output when creating a finished advisor file

Return a complete markdown file using `references/advisor-template.md`.

Do not skip sections. If information is uncertain, state the limitation and define the advisor role based on public, stable, high-level patterns rather than unverifiable claims.
