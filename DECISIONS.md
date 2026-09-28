# Decisions

A running log of the choices made on this project and why, in the order they happened. This is a journal, not a spec — keep adding to it as the project changes. If a later decision overturns an earlier one, don't delete the old entry; add a new one and link back to it, so the history of *why* stays readable.

## How to add an entry

Copy this block to the top of the log below (newest first), fill it in, and commit it in the same commit or PR as the change it describes:

```markdown
## YYYY-MM-DD — Short title of the decision

**Context.** What situation or problem made this decision necessary.

**Decision.** What was decided, in one or two sentences.

**Why.** The reasoning — evidence, trade-off, or constraint that tipped it.

**Alternatives considered.** What else was on the table, and why it lost.

**Status.** Decided / Revisit later / Superseded by [link to a later entry].
```

Keep entries short. If a decision needs a long explanation, put the detail in `docs/research/` and link to it from here.

---

## 2026-09-28 — Rebuild as a browser game, not a Python 2 fix

**Context.** The original `game.py` was a ~20-line Python 2 terminal quiz. Python 2 reached end of life in 2020, and the terminal format limits who can play it.

**Decision.** Rebuild as a single-file browser game (`index.html`), playable with no install, hosted on GitHub Pages.

**Why.** Removes the install barrier entirely and reaches phones. A browser game can also show real feedback (drag-and-drop, contamination, sound) that a terminal quiz can't.

**Alternatives considered.** Port to Python 3 and keep it a terminal game (kept the audience too narrow); build in Godot or Unity (more powerful, but overkill for a 10-item sorting loop and adds a build step this project doesn't need yet).

**Status.** Decided. Original code kept at `legacy/game.py` for history.

---

## 2026-09-28 — Drop the "recyclable" bin; no single universal bin scheme

**Context.** The original game had five bins (plastic, biodegradable, recyclable, paper, glass). "Recyclable" overlaps with plastic, paper and glass, and no real-world sorting system in any of the ten countries researched uses this scheme. Several items (broken window glass, used tissues) had **no correct bin** under it.

**Decision.** Remove the universal 5-bin scheme. Each country gets its own set of bins, matching how that country actually sorts waste.

**Why.** A game that teaches the wrong bin for real items (window glass → glass bin) does active harm — a slicker version of a wrong answer is still wrong. Real bin schemes differ enough (India: wet/dry/sanitary/special care; Sweden: by material; France: nearly everything in one yellow bin) that forcing one scheme onto all of them means someone always gets a wrong answer.

**Alternatives considered.** Keep one scheme and mark ambiguous items as "it depends" (still teaches a wrong default); invent a new "ideal" scheme not used anywhere (defeats the point of teaching real rules).

**Status.** Decided.

---

## 2026-09-28 — Country rules live in data files, not in code

**Context.** Once there's more than one country, the bins and answers can't be hardcoded per-region inside the game logic without the file becoming unmaintainable.

**Decision.** Each country is a JSON file in `data/regions/`, with its own bins, per-item answers, and a `sources` list of the official pages used. A small script (`tools/build_regions.py`) merges them into `index.html`.

**Why.** Separating content (what's true about a country's rules) from code (how the game plays) means adding or correcting a country doesn't touch the game logic, and every claim in the game can be traced to a source.

**Alternatives considered.** One big shared JSON fetched at runtime (adds a network dependency; the whole point was "no install, just open the file"). Hardcoding regions as JS objects in `index.html` directly (works for 2 countries, unreadable at 10).

**Status.** Decided.

---

## 2026-09-28 — Explain every answer, right or wrong

**Decision.** After every sort, show a one-line reason — not just "correct" or "wrong".

**Why.** Feedback that explains *why* measurably beats plain right/wrong feedback in learning research, and a National Geographic waste-sorting game was criticized by reviewers for promising facts and never delivering them. The goal is players learning the *rule*, not memorizing 28 items.

**Alternatives considered.** Show the reason only on mistakes (weaker — reinforcing why a correct answer is correct matters too, especially for "varies locally" items with more than one right answer).

**Status.** Decided.

---

## 2026-09-28 — No lives, no punishing streaks, no leaderboards

**Decision.** Progression uses in-shift combos, personal bests, and forgiving streaks. No hearts/lives, no daily streak that breaks and punishes you, no global leaderboard comparing players.

**Why.** A randomized trial of a similar waste-sorting game found that comparing players against each other *reduced* their confidence in sorting correctly — the opposite of the intended effect. There's also no learning evidence for lives/hearts, and punishing streaks are a known way to make people quit rather than return.

**Alternatives considered.** A global leaderboard for engagement (rejected on the evidence above); daily streaks like Duolingo's (kept the *idea* but made it weekly and forgiving instead of daily and punishing).

**Status.** Decided. Worth re-testing if the game grows a social/classroom feature later — cooperative goals ("our class diverted 100kg") are the safer version of "compare yourself to others."

---

## 2026-09-28 — Bins get a pattern and icon, never color alone

**Decision.** Every bin has a color, a pattern (stripes, dots, grid, etc.), an icon, and a text label — colour is never the only way to identify it.

**Why.** Game accessibility guidelines are explicit that color alone must never carry essential information, and bin colors aren't even consistent between countries (green means "organics" in parts of Europe and "recyclables" in parts of the US), so leaning on color would actively mislead.

**Status.** Decided.

---

## Open questions / revisit later

Things flagged during design that aren't decided yet — move these into dated entries above once resolved.

- **Carbon/water footprint numbers (the "Where did it go?" roadmap item).** Needs its own research pass before any number ships — see the caution in `docs/research/Building a great sorting game.md` about not showing precise-looking numbers backed by weak data. Water footprint data in particular is patchy and shouldn't ship until it's as solid as the carbon numbers.
- **Whether "varies locally" items should let players pick their own city's answer**, or stay at the country level. Country-level was the pragmatic v1 choice; a city-level lookup would be more accurate but is a much bigger data effort.
- **Spaced repetition upgrade path.** Currently a simple Leitner-style box per item, stored in `localStorage`. Duolingo's half-life regression is the documented upgrade if session data ever shows the simple version isn't working.
