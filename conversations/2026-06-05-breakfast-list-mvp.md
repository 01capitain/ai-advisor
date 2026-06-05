---
title: Breakfast-List (TAP) MVP — pressure-test & value
date: 2026-06-05
session_id: 3ad75bd2-3562-4bff-9148-04dd31669a21
advisors_involved:
  - dana-perino
  - marty-cagan
  - mark-cuban
  - horst-schulze
  - dj-patil
  - laszlo-bock
---

# Breakfast-List (TAP) MVP — Advisory Board Conversation

> Structured transcript of a terminal-conducted board conversation. Source of
> record for the `advisory-board.html` presentation layer. Section markers
> (`### User`, `### Dana · Calibration`, `### Dana · Briefing`,
> `### Dana · Advisor Prompt`, `### Advisor · <Name>`,
> `### Dana · Executive Summary`) are parsed by the build script.

## Turn 1 — Pressure-test the MVP plan against achievability · 2026-06-05

### User

Question the targeted plan against achievability. I want to make the
development/pilot phase a success and make sure the breakfast-list becomes a
success both from a project perspective and an economical perspective. We have a
past of missed launches — product/dev teams have not released a successful
product in a while, and it is becoming significantly negative on the team.
Besides success, the project should also provide good insight into how to
improve our release process.

The MVP idea: ship a breakfast-list (TAP / ticket-access) feature to real hotels
fast. The deck lays out six problem scopes to settle before MVP — Setup, Opening
the day, Closing, Analytics, Mobile, and the API — under the motto "Minimal.
Viable. Product, not Most. Valuable." The recommended MVP locks four choices:
**Source = Room list, Prepared opening, Tear-down closing, Live progress
analytics** — keeping connectivity and PMS complexity off the critical path. It
closes by arguing for going out early — early feedback, features built on real
requests, closer client relationships, steering before it's overbuilt —
"GET. SHIP! DONE."

### Dana · Calibration

**Request quality: strong, but I'm sharpening one thing before forwarding.** You've
given the board a real decision, real context, named options, and a clear ask.
That's rare. The single weakness — and it's the one that matters most given your
history — is that **"success" is defined three ways at once**: project success,
economic success, and release-process insight. A team coming off a streak of
missed launches that is told to hit all three equally will hedge, broaden scope,
and slip again. So I'm forwarding the request with this framing attached.

### Dana · Briefing

- **Decision:** Is this MVP scope (four locked picks) the right bet to (a)
  actually ship, (b) succeed in real hotels and economically, and (c) teach you
  something about *why* you've been missing launches?
- **The buried tradeoff:** Your four picks were all chosen to minimize
  **build/technical risk** (PMS and connectivity off the critical path). None
  were chosen to minimize **value or adoption risk**. That's the gap I want the
  board to press on.
- **The morale subtext is the real client.** This launch is as much an
  intervention on the team as on the product.
- **Desired output:** Critique and pressure-test against achievability — not
  validation.

I kept the panel to five, and I deliberately set up the central tension between
**Cagan (validate first)** and **Cuban (ship and sell now)** — your plan leans
hard toward Cuban, and I want it tested.

| Advisor | Why on this question |
|---|---|
| Marty Cagan | Is the MVP *viable*, or just *minimal*? Your slogan quietly drops the V. |
| Mark Cuban | "Economic success" needs a buyer and a number, not a ship date. |
| Horst Schulze | A breakfast/ticket-access tool lives or dies at the 7am rush, in the service moment. |
| DJ Patil | You asked for release-process insight — that has to be instrumented, not hoped for. |
| Laszlo Bock | The missed-launch streak is a systems problem about the team, not just this feature. |

### Dana · Advisor Prompt

> A team with a history of missed launches plans to ship a breakfast-list
> (ticket-access) MVP to real hotels fast. The locked scope — Room-list source,
> prepared opening, tear-down closing, live-progress analytics — was chosen to
> keep PMS/connectivity off the critical path. Pressure-test this plan against
> *achievability*: will it succeed as a project and economically, and will it
> yield insight into a broken release process? Each of you: attack the plan from
> your mandate, name the risk it ignores, and give one concrete corrective. Do
> not validate — critique.

### Advisor · Marty Cagan

**Summary:** Your four picks killed the cheapest risk — build — and left value and adoption wide open. Minimal to build is not the same as minimal to learn, and a room list is not a breakfast entitlement.

Your framing is honest and I respect it — but look at what your four picks
actually optimize for. Room-list source over PMS, prepared/tear-down lifecycle,
live-progress analytics — every one of those reduces **feasibility risk**. That's
the *cheapest* risk you have. You've engineered the easy risk down to zero and
left the expensive ones untouched:

- **Value risk:** Where is the evidence that "live progress" on a breakfast list
  is a top pain for the people running breakfast — versus a dashboard a manager
  wanted? "Tear-down closing" and "prepared opening" sound like a roadmap, not a
  validated job-to-be-done.
- **Data-value risk:** A *room list* is not a *breakfast entitlement*. A room can
  be booked with or without breakfast included. If the real job is ticket-access
  — who's entitled — then sourcing from the room list may make the build trivial
  and the product wrong. That's the classic "minimal but not viable" trap.

The fix isn't to add PMS back. It's to pick the scope that most reduces your
**highest** risk. Right now your highest risk is: *does live breakfast-progress
tracking change how a real hotel runs service?* Run a one-week discovery against
3–5 hotels before you lock, and define — in writing — what you'd have to observe
in the pilot to call this validated. A successful *pilot* is not the same as a
successful *launch*. If you ship and breakfast service runs exactly as it did on
paper, would you even know you'd failed?

### Advisor · Mark Cuban

**Summary:** “Economic success” means nothing until a real hotel says yes to a real number — get 5–10 pilots committed before you build, not after. Shipped-and-abandoned is your worst outcome; a customer who won’t give it back is the morale cure.

I like the energy — "GET. SHIP! DONE." beats another six-month roadmap funeral.
But "economic success" is doing a lot of work in your sentence and nobody's
defined it. Answer this before you write more code:

1. **Is this a new paid module, or bundled into the existing subscription?** If
   it's bundled, your economic success metric isn't new revenue — it's retention
   and expansion, and you should say so. If it's a paid add-on, what's the price,
   and has *one human being at a hotel* said yes to that number?
2. **Get the pilot hotels committed before you build, not after.** Five to ten
   properties who'll run it in a real shift and tell you the truth. Not a survey
   — a phone call. You have the installed base; use it as a lab.
3. **Don't let "shipped" be the win.** Shipped-and-abandoned is your *worst*
   outcome here — it confirms the team's fear that they can't land anything. The
   win is a hotel that keeps using it after the pilot, ideally paying for it.
   That's the morale cure: not a clean launch, a customer who won't give it back.

Where I'll push back on Cagan: don't disappear into a discovery sprint. Do both
in the same week — three calls *are* your discovery and your sales motion at once.

### Advisor · Horst Schulze

**Summary:** A ticket-access list at the dining-room door is a checkpoint — you’ve designed distrust into the warmest moment of a guest’s morning. The only test that counts is the 7am rush; if the host reaches for paper, you’ve failed.

Be careful what you've designed. "TAP / ticket-access" plus a "room list" source
plus "live progress" can very easily become a **checkpoint at the dining room
door** — the moment a guest sits down to eat, your staff is verifying them against
a list. That is distrust, designed into the warmest moment of a guest's morning.

Two operational truths your plan must survive:

- **The 7am rush is the only test that counts.** "Prepared opening" and
  "tear-down closing" each add a daily ritual. If setting up or tearing down
  steals two minutes during the breakfast crush, the host will abandon your
  tablet for the printed list and never come back. The real pilot metric is
  physical: at the busiest twenty minutes, does the staff reach for your tool or
  for paper?
- **Live progress is for whom?** If it helps the host on the floor serve faster,
  beautiful. If it's a manager watching a dashboard from the office, you've
  shipped surveillance and called it a feature. Ask which it is before you build
  it.

Design entitlement to resolve **quietly in the background** — serve first,
reconcile later, exceptions go to a manager, never to the guest's table. If you
can't build it that way for the MVP, that scope isn't ready and it should not
touch the dining room.

### Advisor · DJ Patil

**Summary:** Commit three product metrics and three process metrics in writing before launch, and never move the goalposts after the data lands. You asked to learn why launches keep failing — then instrument the release, not just the product.

You asked for two outcomes that need two different instruments, and most teams
only build the first one.

**Product success — pick three, set thresholds before launch, write them down:**

1. **Weekly active hotels** — properties that used it in a *real shift*, not
   onboarding. Below threshold at 8 weeks = adoption problem.
2. **Core-flow completion without fallback** — of breakfast services started in
   the tool, how many finished without reverting to paper/WhatsApp. This tells
   you whether you're a real workflow or a parallel system.
3. **Support contact rate per active hotel** — if it climbs with usage, you're
   shipping confusion.

Given your history, the discipline that matters most: **commit the thresholds in
writing now and refuse to move the goalposts after the data lands.** A
morale-hungry team will be tempted to redefine success at the finish line. Don't.

**Release-process insight — this is the part you'll skip if I don't insist.** You
said you want to learn how to improve releases. Then instrument the *release*,
not just the product:

- Cycle time: decision-locked → live in a real hotel.
- Scope changes after the lock (count them — this is almost certainly your
  historical failure signature).
- Defects/blockers found in pilot vs. caught before.
- Time-to-first-real-use per pilot hotel.

Run this launch as a designed experiment with the retro scheduled on day one. A
pilot that ships but isn't instrumented teaches you nothing about why the last
several didn't.

### Advisor · Laszlo Bock

**Summary:** The missed-launch streak is a system signal, not a talent problem — make this launch small enough that it cannot miss. Define “done” as used in one real shift, lock the scope, and break the streak with one undeniable early win.

Step back: the actual subject of this brief is the team, and the feature is the
instrument. Three observations on the system you're operating in:

1. **Make this launch small enough that it cannot miss.** The single most
   powerful design choice available to you is shrinking the definition of "done"
   until success is nearly guaranteed. "Done" = *in real hotels' hands, used in a
   real shift.* Not feature-complete, not all six scopes — used, once, for real.
   A streak of misses is broken by one undeniable, early, visible win, not by a
   perfect product.
2. **Three success definitions is itself a way to miss.** A demoralized team told
   to hit project success *and* economics *and* process learning will spread thin
   and slip — exactly the pattern that hurt them before. Pick **one primary**
   (I'd argue: *used in a real shift in N hotels by date X*) and let the others
   be secondary.
3. **Protect the scope lock like it's the product.** Your historical failure
   signature is almost certainly scope creep or a moving definition of done —
   Patil's "scope changes after lock" metric will prove it. Put a visible, short
   feedback cadence in place so the team sees progress accumulate. Morale
   compounds from visible wins, and the process insight you want falls out
   naturally if you run this as a deliberate, retro'd experiment rather than a
   hope.

The board-design caveat, since it's my mandate: I'm answering here on
team-effectiveness, which is squarely in my domain — but if you later want the
*release process itself* redesigned as a standing capability, that's a larger
engagement than one feature.

### Dana · Executive Summary

The board does **not** disagree about shipping fast — Cuban, Cagan, and Laszlo
all want this out the door. They disagree about **what you've de-risked**, and
they converge on one diagnosis:

> **Your four picks minimized the cheapest risk (build/technical) and left the
> expensive ones — value, adoption at the service moment, and a defined success
> criterion — completely open.** That is the exact recipe for a launch that
> "ships" and then quietly fails, which for this team would be worse than not
> shipping at all.

The agreements are louder than the tensions:

- **Cagan + Horst:** the "room list" source and the live-progress/lifecycle picks
  may be easy to build and wrong for the job — entitlement ≠ room, and a
  checkpoint at the table kills adoption.
- **Patil + Laszlo:** define success in writing *before* launch, lock scope, and
  don't move goalposts — and instrument the *release* itself, or you'll waste the
  one chance to learn why you keep missing.
- **Cuban + Laszlo:** the morale cure isn't a clean ship; it's a hotel that won't
  give the tool back. Get pilots committed before building.

The one genuine tension — Cagan's "validate first" vs. Cuban's "ship now" —
resolves the same way both men actually argue it: do both in the same week. Three
to five real hotel conversations *are* the discovery and the pilot recruitment at
once. You don't need a sprint; you need a phone.

**Recommended next decision** — Before any further build, produce a one-page
**pilot contract** — and given your history, this is the artifact that breaks the
streak:

1. **One primary success definition** (recommend: *used in a real breakfast
   shift, unassisted, in N committed hotels by [date]*), with economics and
   process-insight named as explicit secondaries.
2. **5–10 named pilot hotels**, verbally committed before you build (Cuban's
   call).
3. **Three product metrics + three process metrics, with thresholds
   pre-committed in writing** (Patil), and a hard scope lock with a
   change-counter.
4. **One operational design ruling:** entitlement resolves in the background,
   staff serve first and reconcile later (Horst) — decided now, because it
   determines whether "room list" source is even acceptable.
5. **A retro scheduled on day one**, so the release-process insight is captured
   by design rather than reconstructed from memory.

Lock that page, then "GET. SHIP! DONE." — but ship *that* scope, and don't touch
it.

## Turn 2 — What is the value of a breakfast list to hotels? · 2026-06-05

### User

What is the value of a breakfast list for hotels — why are they doing it
currently and why would they pay for a digital tool? Is it guest validation, or
analytics (hardly achievable without a digital process — yet hotels are still
asking guests for their room number when entering)?

### Dana · Calibration

Approved — and I'm reframing it, because the question you're really asking is a
positioning decision. "What is the value of a breakfast list?" is the surface;
underneath it is *"what do we sell this on, and what do we merely include?"* That
answer drives your MVP scope, your pricing, and your pilot-hotel selection.

One piece of evidence is already sitting in your own question and it's the
sharpest thing here: **hotels currently ask guests for their room number at the
door.** That is not a hypothetical — it's observed behavior, every morning, in
thousands of properties. It tells you the *validation* job is real and currently
done manually. Nobody is manually computing breakfast *analytics*, which tells
you something equally important about that side.

### Dana · Briefing

- **Decision:** Is the core value proposition guest/entitlement validation, or
  analytics?
- **What to pressure-test:** Which value a hotel will actually pay for *today*,
  versus which value only becomes possible *after* they've gone digital.
- **Output:** A ranked value hypothesis and the two or three things to verify
  with real hotels.

**Panel:** Horst (why they do it today), Cagan (what the real job is), Cuban
(what opens the wallet), Patil (whether analytics can be the wedge).

### Dana · Advisor Prompt

> Why do hotels keep a breakfast list today, and why would they pay for a digital
> version? Currently they ask guests for a room number at the door. Settle
> whether the core value is **entitlement/guest validation** or **analytics** —
> and note that analytics is hard to deliver without first owning a digital
> process. Each of you answer from your mandate: what is the job, what opens the
> wallet, and what is merely a nice-to-have?

### Advisor · Horst Schulze

**Summary:** The room-number question is loss prevention wearing the costume of hospitality — breakfast isn’t free to the hotel and isn’t included in every rate. Make validation invisible and graceful; analytics is a number management looks at, and the front line will never care.

Let me tell you what the room-number question actually is: it is **loss
prevention wearing the costume of hospitality.** Breakfast is not free to the
hotel — there's food cost and staff cost — and it is *not included in every
rate.* Some guests booked room-only, some booked bed-and-breakfast, some are
walk-ins. So the hotel keeps a list (a printed report from the PMS) and asks the
room number to answer one question: *are you entitled, or do I charge you?*

That is the job today, and it is done by interrogating the guest at the warmest
moment of their morning. So the value of your tool is **not** to add a checkpoint
— it's to make that validation **invisible and graceful** while still protecting
the revenue. The hotel will pay to stop giving breakfast away *and* stop policing
its guests at the same time. Analytics? That's a number management looks at in
the office. The host at the door will never care about it — so do not build your
value story on it.

### Advisor · Marty Cagan

**Summary:** “Breakfast list” is a solution; the real jobs are revenue protection, food forecasting, and service throughput. Hotels already validate manually every day — strong evidence — while analytics is an unproven bet, so don’t lead with it.

"Breakfast list" is a solution. There are three underlying jobs, and they don't
weigh equally:

1. **Don't give away breakfast you should have charged for** (revenue
   protection).
2. **Prepare the right amount of food** (forecasting / waste).
3. **Get guests fed quickly and warmly** (service throughput).

Here's the evidence test, and your own question passes it beautifully: hotels
*demonstrably already do* job #1 — manually, every day, by asking room numbers.
That's **observed behavior**, the strongest kind of validation signal. Analytics
has the opposite signature: **no hotel is doing it manually today.** That doesn't
make it worthless, but it tells you it's an *unproven bet*, not a felt pain. You
don't lead with the bet. You lead with the job they're already paying staff to do
badly.

Caveat: the top job varies by segment. A resort where breakfast is included for
everyone has no validation pain — their job is forecasting and groups. So "the
value" isn't one answer; it's a function of the hotel's rate mix. Pick your wedge
segment deliberately.

### Advisor · Mark Cuban

**Summary:** Put euros on it — 5% of 100 covers eaten free at €15–25 is €2–4k/month walking out the door, and that opens a wallet; a dashboard does not. Validation is the painkiller you sell on; analytics is the vitamin that reduces churn after the deal.

Put euros on it or it's not a value prop. A hotel doing 100 covers a morning,
with even 5% eating free who should've been charged at €15–25 a head — that's
**€2,000–€4,000 a month walking out the door.** Plus food they over-prepped and
threw away. *That* opens a wallet. "Beautiful analytics dashboard" does not.

So the answer to your question is blunt: the thing they'll **pay for** is the
painkiller — stop the leak, stop the door friction, stop the manual
reconciliation with the PMS. Analytics is a vitamin. Vitamins don't close deals;
they reduce churn after the deal.

Go validate the price in ten phone calls. Ask each hotel two questions: *"How do
you handle breakfast for a room-only guest today?"* and *"How often does someone
eat who shouldn't have?"* Their answers will price your product better than any
deck. If they can't quantify the leak, your wedge is door-friction and food waste
instead — but you'll know in two days.

### Advisor · DJ Patil

**Summary:** You’re right that analytics can’t be the wedge — you can’t deliver it without first owning the digital process, so it’s the flywheel. Only analytics tied to a euro decision matter, and the revenue-capture metric is what sells year two.

Your instinct in the question is exactly right, and it's the crux: **you cannot
deliver analytics without first owning the digital process — so analytics cannot
be the wedge. It's the flywheel.** Today the hotel runs blind; the moment they go
digital *for validation*, the data starts accruing as a byproduct, and *that*
becomes your switching cost.

But be ruthless about which analytics matter — only the ones tied to a euro
decision:

- **Covers forecast** → how much food to order (waste reduction, real money).
- **No-show / actual-vs-expected** → over-prep correction.
- **Peak-time curve** → staffing decisions.
- **% paid vs. included** → the revenue-capture number that proves your own ROI
  back to the buyer.

Everything else — "who ate, prettily charted" — is vanity and won't survive a
renewal conversation. So: analytics doesn't sell the first contract, but the
*revenue-capture metric* is what lets you walk back into that hotel in month
three and say "here's the €3,100 we recovered" — and that's what sells the
*second* year and the next ten hotels.

### Dana · Executive Summary

The board is unusually aligned, and your hunch is correct:

| | **Validation / revenue protection** | **Analytics** |
|---|---|---|
| Done manually today? | **Yes** — room-number checks | No |
| Opens the wallet? | **Yes** (the painkiller) | No (the vitamin) |
| When is it valuable? | Day one | Only *after* the digital process exists |
| Role | **The wedge — why they buy** | **The flywheel — why they stay** |

- **The pay-today value is entitlement validation + revenue-leakage protection +
  removing door friction.** The fact that hotels interrogate guests for a room
  number every morning is your proof the job is real, manual, and unsolved.
- **Analytics is a consequence, not a cause.** You can't offer it until you own
  the process, and it only sells the *renewal*, anchored on the one metric that
  shows recovered revenue.
- **The productive tension** is Horst vs. Cuban: Cuban says sell the
  leak-stopping; Horst warns you must never sell "police your guests." They
  reconcile in one line — **"protect the revenue without policing the guest"** —
  which is also the design constraint (entitlement resolves quietly, as Horst
  argued on the MVP).
- **Segment matters:** willingness to pay is highest at **mixed-entitlement,
  higher-volume hotels** where breakfast is a meaningful revenue/cost line.
  Included-for-everyone resorts have a different (forecasting) value and shouldn't
  anchor your wedge.

**Recommended next decision** — Lock the value proposition as **"protect
breakfast revenue and the welcome — without the door interrogation,"** with
analytics positioned explicitly as the retention/ROI story, not the sales hook.
Then verify with ~10 mixed-rate hotels the two numbers that price it: **their
estimated breakfast leakage** and **how they handle/charge room-only guests
today.** Steer the pilot toward that segment.
