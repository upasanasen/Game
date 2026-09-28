# Rebuild the sorting quiz around learning

The upasanasen/Game quiz already has the core of a good sorting game: show an item, ask for a bin, keep score. That is essentially the design a University of British Columbia study used, which **raised sorting accuracy from 69% to 84%** and held up a week later ([UBC Psychology](https://psych.ubc.ca/news/online-game-trains-players-how-to-sort-waste-correctly/)). Three things stop it from being a great game. Its content teaches wrong answers. Its feedback is bare right/wrong. It runs on Python 2, which has been dead since 2020. The five bins (plastic, biodegradable, recyclable, paper, glass) match no real-world scheme, and they overlap, because plastic, paper and glass are all "recyclable". None of the five is correct for broken window glass in India, Sweden or the US/UK. Used tissues belong in India's "sanitary" stream, which the quiz doesn't have. The research points to a clear set of components:

- **An immediate "why" line after every answer.** Feedback averages d ≈ 0.48, and elaborated feedback beats right/wrong.
- **A scheduler instead of `random`.** It spaces, interleaves and bags items fairly, which directly targets retention.
- **Region-aware, data-driven content** with a residual-waste option.
- **Moderate "juice"**, meaning audiovisual feedback. It measurably increases playtime, but only up to a point.
- **Accessibility and progression that avoid dark patterns.** Bins identified by colour plus icon plus label, and no punishing streaks.
- **A Python 3 → pygame-ce → pygbag stack** that ships a zero-install browser build to itch.io and GitHub Pages.

The stakes are real: 84% of UK households contaminate their recycling at least once, and the main cause is uncertainty, not apathy ([WRAP](https://www.wrap.ngo/media-centre/press-releases/84-uk-households-are-unintentionally-contaminating-their-recycling-bins)). A game that answers "which bin, and why, where I live?" is filling a real gap.

A caveat on scope: this report works from the repo description supplied with the question (about 20 lines, 15 items, 10 random rounds, empty README, MIT licence). It did not inspect the code line by line. The item-accuracy analysis below covers the six named items. The other nine need the same audit.

## Great games turn a rule set into a feeling of mastery

The major design frameworks converge on one idea: players experience a game as emotion, and rules only matter insofar as they produce that emotion. The MDA framework splits a game into Mechanics, Dynamics and Aesthetics. Designers build from mechanics upward, while **players experience it from aesthetics downward** ([MDA paper](https://users.cs.northwestern.edu/~hunicke/MDA.pdf)). For a sorting game, the target aesthetics are Challenge (getting sorts right), Discovery (surprising facts, such as the EPA saying greasy pizza boxes are recyclable once scraps are removed) and Sensation (a satisfying drop). Raph Koster puts it more bluntly: "fun is just another word for learning". Games are patterns the brain chunks, and they turn boring once the pattern is mastered ([Theory of Fun summary](https://game-studies.fandom.com/wiki/A_Theory_of_Fun_for_Game_Design)). This is the quiz's structural problem. With 15 fixed items, the pattern is mastered after a few plays, so the game needs a supply of new, ambiguous and region-specific items to keep teaching.

Motivation research gives the same message from another angle. Ryan, Rigby and Przybylski found that **perceived competence, autonomy and relatedness each independently predicted enjoyment and intention to replay** ([SDT paper](https://selfdeterminationtheory.org/SDT/documents/2006_RyanRigbyPrzybylski_MandE.pdf)). Jenova Chen's flow work argues for keeping challenge matched to skill, and for letting players choose difficulty through the mechanics rather than through hidden adjustment ([Chen thesis](https://www.jenovachen.com/flowingames/Flow_in_games_final.pdf)). Nicole Lazzaro's "4 Keys" map neatly onto this game ([Lazzaro](https://www.nicolelazzaro.com/the4-keys-to-fun/)). Hard Fun comes from accuracy, Serious Fun from a real-world skill, Easy Fun from quirky items, and People Fun from optional cooperative sharing.

The core loop should borrow from the best quick-decision games. King's Candy Crush team uses a **"complexity staircase"** that introduces one new blocker at a time and deliberately follows a hard level with a lighter one. It also treats fun and difficulty as separate metrics: "the longer the level is, the less likely it is to be fun", and "crazy hard levels never pay off" ([PocketGamer.biz](https://www.pocketgamer.biz/crafting-candy-crushs-difficulty-blockers-level-design-ai-and-the-complexity-staircase/); [MobileGamer.biz](https://mobilegamer.biz/how-king-defines-a-good-candy-crush-saga-level-and-why-it-constantly-prunes-the-bad-ones/)). Papers, Please is the closest genre analogue: inspect, classify, stamp. Lucas Pope layered new rules in day by day. Playtesting showed players ignored rule bulletins that arrived while a character was talking, so he moved new rules to quiet moments ([Game Developer](https://www.gamedeveloper.com/design/designing-the-bleak-genius-of-i-papers-please-i-)).

Randomness needs taming too. Tetris's **7-bag randomizer** exists because naive randomness produces "droughts" that feel unfair ([TetrisWiki](https://tetris.wiki/Random_Generator)). For this quiz, that argues for replacing `random.choice` over 15 items with a bag that guarantees every bin appears (for example, two items per bin across 10 rounds), orders items easy-to-ambiguous with breathers in between, and never repeats an item within a session. Instructions should stay WarioWare-short: each microgame opens with a one- or two-word command ([Mario Wiki](https://www.mariowiki.com/Microgame)). "Sort it!" is enough.

## Feedback that explains outperforms feedback that dazzles

Two bodies of evidence meet at the moment the player drops an item in a bin, and together they define what that moment should contain.

The first is game feel. Steve Swink defines responsive control as a response inside a correction cycle of **under about 100 ms**, with polish (art, sound, animation) selling the interaction ([Wikipedia: Game feel](https://en.wikipedia.org/wiki/Game_feel)). Jonasson and Purho's "Juice it or lose it" talk showed that tweens, particles and sound turn a flat Breakout clone into an engaging one ([YouTube](https://www.youtube.com/watch?v=Fy0aCDmgnxg)). The best controlled evidence shows an inverted U. In Kao's 2020 study of **3,018 players**, both no juice and extreme juice significantly lowered playtime, intrinsic motivation and performance compared with medium or high juice ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1875952118300879)). A CHI 2024 follow-up found **curiosity was the strongest predictor of enjoyment and the only predictor of playtime**, and it supported feedback that depends on success ([ACM DL](https://dl.acm.org/doi/10.1145/3613904.3642656)). In practice:

- A correct sort gets a snap, a squash-and-stretch bin, a distinct sound and a small particle burst, with the pitch rising on combos.
- A wrong sort gets a gentle shake and a different sound, never a punishing effect.
- Nothing ever obscures the next item.

The second is learning feedback. Across 435 studies, feedback averages **d = 0.48**, and its impact depends on how much information it carries: **elaborated feedback beats knowledge-of-results** ([Wisniewski, Zierer & Hattie 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full)). The UBC game's key feature was that a wrong answer immediately showed the correct bin ([PubMed 30502613](https://pubmed.ncbi.nlm.nih.gov/30502613)). Reviewers of National Geographic's Recycle Roundup complained that its promised facts never arrived, and one said "I didn't actually learn" ([EarthPlex](https://www.earthplexmedia.com/2021/04/recycle-roundup-game-review-.html)).

The synthesis is a one-line, non-moralising "why" card after every answer, correct ones included, because it reinforces the rule rather than the single item. Two examples:

- "Window glass melts differently from bottle glass, so one pane can spoil a batch."
- "Used tissues: fibres too short and soiled to recycle."

No study was found that isolates "explanation plus feedback" against "feedback only" for waste sorting specifically. The general feedback literature strongly favours the richer version.

Onboarding follows the same principle: teach by doing. Celia Hodent recommends teaching a mechanic only when the player can use it immediately, avoiding early punishment, and remembering that learners hold only about three items in working memory ([Celia Hodent](https://celiahodent.com/gamers-brain-ux-onboarding/)). Round 1 should therefore be the tutorial. It uses an obvious item with the correct bin gently highlighted and no penalty. Five bins exceeds a novice's working memory, so every bin needs an icon and a word, not just a colour.

## Learning science supplies the progression system, and Duolingo supplies the cautions

Meta-analyses set realistic expectations. Serious games beat conventional instruction by about **d = 0.29 for learning and d = 0.36 for retention**, but their motivational advantage (d = 0.26) is **not statistically significant** ([Wouters et al. 2013](https://eric.ed.gov/?id=EJ1008015)). The moderators that raise gains are multiple sessions, supplementary instruction and group play. Design choices within a game matter about as much as the choice to use a game at all: "value-added" versions of the same game gained **g = 0.34** over their plain versions ([Clark et al. 2016](https://journals.sagepub.com/doi/10.3102/0034654315582065)). A single 10-round session is the weakest setup this literature describes. The way to improve it is return visits with smart scheduling.

The quiz format is already sound. Retrieval practice beats restudy (g = 0.51), and **multiple-choice practice tests reach g = 0.70** ([Adesope et al. 2017](https://journals.sagepub.com/doi/abs/10.3102/0034654316689306)). Three mechanics would build on it.

**Spacing.** The optimal gap between reviews grows with how long you want people to remember ([Cepeda et al. 2006](https://augmentingcognition.com/assets/Cepeda2006.pdf)). Duolingo's half-life regression models recall as p = 2^(−Δt/h) per item, and **raised daily engagement by 12%** in production ([Settles & Meeder 2016](https://research.duolingo.com/papers/settles.acl16.pdf)). The open-source code and data are available on [GitHub](https://github.com/duolingo/halflife-regression). A Leitner box per item is the simple version, and HLR is the upgrade.

**Interleaving.** It helps most when categories are similar or confusable ([Brunmair & Richter 2019](https://www.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf)). Waste sorting is exactly that kind of task: a plastic bag versus a plastic bottle, a drinking glass versus a jar, a milk carton versus a newspaper.

**Mastery gating.** Mastery learning averages **d = 0.52**, with larger effects for weaker learners ([Kulik et al. 1990](https://journals.sagepub.com/doi/10.3102/00346543060002265)). In this game, that means unlocking a new material category or "district" only after the rules before it have held up across spaced sessions.

Intrinsic integration is the strongest design argument for this particular game. In Habgood and Ainsworth's Zombie Division, where the maths *is* the combat, children learned more than from a version with bolted-on quizzes and **played about 7× longer by free choice** ([Habgood & Ainsworth 2011](https://tecfa.unige.ch/tecfa/teaching/BSEP/articles/Habgood_Ainsworth_2011.pdf)). Sorting is already the core mechanic. The risk is diluting it with abstract points. The score should instead mean something in the domain: kilograms diverted, or the purity of a recycling "bale" that a mis-sort visibly contaminates. That also echoes how well-reviewed ecogames like Terra Nil "teach through play loops rather than lecturing" ([Digitally Downloaded](https://www.digitallydownloaded.net/2024/01/review-terra-nil-nintendo-switch.html)).

Duolingo's retention tools come with evidence, but for engagement, not learning. The Streak Wager raised **Day-7 retention by 14%**. Streak protection made learners **4% more likely to return** a week later ([Duolingo blog](https://blog.duolingo.com/how-streaks-keep-duolingo-learners-committed-to-their-language-goals/)). A qualitative study documents learners farming easy XP to win leagues at the expense of real learning ([ACM L@S 2022](https://dl.acm.org/doi/abs/10.1145/3491140.3528274)). Zagal, Björk and Lewis catalogue time-gating, pay-to-skip and social-pressure mechanics as dark patterns ([Deceptive.design](https://deceptive.design/articles/dark-patterns-in-the-design-of-games/)).

The most relevant warning comes from the waste domain itself. In "The Waste Game" RCT, a **simplified version outperformed an enhanced version with player matching and score comparison** on confidence in sorting, apparently because being matched against others demotivated players ([The Behaviouralist](https://thebehaviouralist.com/portfolio-item/the-waste-game/)). The right progression set, then, is:

- In-session combos
- Personal bests and per-category accuracy
- Visible "locks" to unlock (following Hodent)
- Forgiving weekly streaks
- XP weighted toward due and hard items
- Cooperative goals in place of global leaderboards

For behaviour rather than knowledge, lower expectations further. In field studies of household recycling, **only social modelling and environmental changes reliably changed behaviour**, and information alone did not ([Varotto & Spagnolli 2017](https://www.sciencedirect.com/science/article/abs/pii/S0272494417300452)). The UBC field test saw only a "slight" drop in contamination. Following Fogg's B = MAP model, where ability is usually the bottleneck ([behaviormodel.org](https://www.behaviormodel.org/)), the game's most valuable real-world features are ones that make the right action easier: a searchable "which bin?" lookup, a local cheat-sheet, and positive peer norms.

## The current five bins teach wrong answers for key items

No universal bin scheme exists, and the quiz's scheme matches none of the real ones. **India's Solid Waste Management Rules 2026**, in force since 1 April 2026, mandate four streams: wet, dry, sanitary and special care ([DD News](https://ddnews.gov.in/en/new-waste-rules-from-april-1-four-way-segregation-mandatory-strict-penalties-for-violations/)). **Tissues and diapers are "sanitary". Broken glass, batteries, bulbs and medicines are "special care"** ([Scroll.in](https://scroll.in/article/1091266/four-way-segregation-landfill-restrictions-will-indias-new-solid-waste-rules-bring-about-change)). Sweden sorts packaging by material. **Milk and egg cartons go in paper packaging**. **Window glass, drinking glasses and mirrors must not go in glass packaging containers** ([Svenska App](https://www.svenska.app/blog/recycling-in-sweden-how-to)). **Used kitchen paper and napkins go to food waste** in many municipalities ([Avfall Hälsingland](https://avfallhalsingland.se/sorteringsguide/matavfall/hushallspapper/)). The US EPA says plastic bags **cannot go in curbside recycling** because they tangle machinery, and used tissues are unrecyclable because the fibres are too short and soiled ([EPA](https://www.epa.gov/recycle/how-do-i-recycle-common-recyclables)). Broken window glass generally goes to landfill because it melts differently from container glass ([Napa Recycling](https://naparecycling.com/guide/glass-broken/)).

| Item in quiz | India (SWM Rules 2026) | Sweden | US/UK typical | Verdict for the 5-bin quiz |
|---|---|---|---|---|
| Polybag | Dry | Plastic packaging | Not curbside; store drop-off | "Plastic" works for India/Sweden and is wrong for US curbside |
| Banana peel | Wet | Food waste | Compost/organics | "Biodegradable" is safe |
| Tetra Pak milk box | Dry/recycling | Paper packaging | Mixed recycling (varies) | "Paper" and "recyclable" are both defensible. Explain that it is multi-material |
| Egg tray (moulded pulp) | Dry (varies) | Paper packaging; also accepted in food waste | Paper or compost | Accept "paper"; note it is compostable |
| Used tissues | **Sanitary** | **Food waste** (many kommuner) | Trash; never recyclable | "Paper" and "recyclable" are wrong everywhere. "Biodegradable" is right only in Sweden-like systems |
| Broken window glass | **Special care** | Recycling centre, not glass bin | Landfill/trash | **No correct bin exists among the five** |

Two structural fixes follow. First, the game needs a **residual/general-waste bin** and, for India, sanitary and special-care options. Otherwise it forces players into a wrong answer. Second, the "recyclable" bin should go, because it overlaps with every material bin. Real schemes split by material (Sweden) or by wet/dry (India), never by "recyclable versus material".

The best fix is a **region selector** (for example "India 2026" with four streams, or "Sweden" with material streams), backed by a data file in which each item carries a correct bin per region. This mirrors what the best real-world sorting apps do. GomiSense, for instance, encodes ward-level rules for Tokyo ([GomiSense](https://gomisense.com/en/blog/best-japan-garbage-app)). Contested items should say "depends on where you live" rather than assert one answer. Even Tetra Pak says cartons are recyclable only "where adequate collection, sorting and recycling infrastructures are in place, at scale" ([Tetra Pak India](https://www.tetrapak.com/en-in/campaigns/go-nature-go-carton/explore/recycle-cartons)).

The item pool should also target real confusion. In the UK, the top contaminant is **drinking glasses (33% of households)**, followed by foil pouches (29%) and toothpaste tubes (26%). The most-missed recyclable is glass perfume bottles (52%) ([WRAP](https://www.wrap.ngo/media-centre/press-releases/84-uk-households-are-unintentionally-contaminating-their-recycling-bins)). These are exactly the confusable pairs that interleaving works best on. Tone matters as well: mistakes should be framed as common and fixable, never as guilt.

## Accessibility, stack and operations are cheap now and expensive later

**Accessibility.** Both the Game Accessibility Guidelines and Xbox guideline 103 state that **colour alone must never carry essential information** ([GAG](https://gameaccessibilityguidelines.com/full-list/); [XAG 103](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103)). Colour-coded bins are exactly the risky case, especially since bin colours differ between countries. Green means organics in much of Europe and recyclables in parts of the US ([AFNOR](https://www.afnor.org/en/news/household-waste-help-standardize-the-bin-color-code/)). Each bin therefore needs:

- an icon
- a text label
- a fixed position
- optionally a pattern

Right and wrong feedback needs an icon, text and a sound, not just green and red. XAG 103 also notes that colour-blindness simulators such as Color Oracle do not replace testing with colour-blind players. Further requirements from the guidelines:

- no timer by default, or an adjustable one
- tap-to-select as well as drag-and-drop, plus number keys 1–5
- large, well-spaced targets
- text names on every item image

**Stack.** Python 2.7 reached end of life on **1 January 2020** ([Python.org](https://www.python.org/doc/sunset-python-2/)), so a Python 3 port comes first regardless of anything else. For someone who works in Python and wants a game people can share, the best fit is **pygame-ce**, which is actively maintained with release 2.5.8 in August 2026 ([releases](https://github.com/pygame-community/pygame-ce/releases)), plus **pygbag**, which packages it as WebAssembly for itch.io and GitHub Pages ([pygbag wiki](https://pygame-web.github.io/wiki/pygbag/)). pygbag's constraints should shape the architecture from day one: an `async def main()` loop that yields each frame, OGG-only audio, assets inside the game folder, and no synchronous I/O. The alternatives each fall short somewhere:

- **Arcade** does not support browsers ([Arcade FAQ](https://api.arcade.academy/en/3.3.3/about/faq.html)).
- **Textual** is the cheapest polish if the game stays a terminal quiz, but its web mode runs server-side ([textual-web](https://github.com/Textualize/textual-web)).
- **Godot 4 with GDScript** is the step up if mobile stores or built-in screen-reader support matter. It has experimental AccessKit support since 4.5 ([Godot 4.5](https://godotengine.org/releases/4.5/)), but C# projects still cannot export to the web ([Godot Forum](https://forum.godotengine.org/t/is-there-an-update-on-exporting-c-projects-to-web/128821)).
- **Phaser 4**, released April 2026, is the web-native choice for JavaScript developers ([GameFromScratch](https://gamefromscratch.com/phaser-4-released/)).

**Architecture.** Robert Nystrom's Game Loop and State patterns cover the menu, play and results flow ([Game Programming Patterns](https://gameprogrammingpatterns.com/contents.html)). The layout should have four parts:

- a pure-Python `core/` for rules, scoring and scheduling, with no pygame imports
- `scenes/` for the screens
- `content/items.json` with per-region bins, explanations, difficulty and locale keys
- a `platform/` layer that saves to a JSON file on desktop and to browser storage on the web

The platform layer should save on every results screen, because `pygame.QUIT` doesn't fire in the browser ([PyScript docs](https://docs.pyscript.net/2026.3.1/user-guide/pygame-ce/)). pygbag's exact storage API was not verified in this research.

**Testing.** Unit-test `core/` with pytest. Run scene smoke tests headless by setting `SDL_VIDEODRIVER=dummy` ([pygame wiki](https://www.pygame.org/wiki/HeadlessNoWindowsNeeded)). Add a bot that plays thousands of sessions to catch crashes and to flag items that are unfairly hard. That bot is the equivalent of King's per-level "time to pass" and "time to abandon" metrics. A GitHub Actions job should run the tests and a pygbag build on every push. That workflow is inferred and was not taken from a published template.

**Assets.** Kenney's packs are **CC0 and commercially usable** ([Kenney](https://kenney.nl/support)), and Freesound lets you filter by CC0 ([Freesound FAQ](https://freesound.org/help/faq/)). Keep a licence file listing every asset.

**Analytics.** If children might play, the amended **COPPA rule has been enforced since 22 April 2026** ([Federal Register](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)). The safe default is to collect no personal data. Log anonymous per-session events (item, chosen bin, correct, response time) and send only aggregates. Use cookieless page analytics such as Plausible ([Plausible](https://plausible.io/cookieless-web-analytics)), keeping in mind that GDPR still applies and no regulator has certified "no banner needed" ([CookieBeam](https://cookiebeam.com/guides/plausible-fathom-cookieless-analytics-consent-2026)).

**Distribution.** itch.io HTML5 uploads need a ZIP with `index.html` at the root, and allow up to 500 MB and 1,000 files ([itch.io docs](https://itch.io/docs/creators/html5)). That is far beyond what this game needs.

**Evaluation.** To claim learning, not just fun, follow the Waste Game's design: a pre-test, an immediate post-test and a roughly 3-week delayed test, scored on *unseen* items so it measures rule transfer rather than memorisation. The LM-GM model offers a checklist for mapping each learning mechanic to the game mechanic that delivers it ([Arnab et al. 2015](https://bera-journals.onlinelibrary.wiley.com/doi/abs/10.1111/bjet.12113)).

## Component checklist

| Area | Component | Why (evidence) |
|---|---|---|
| Content | Region-tagged `items.json` (bin per region, one-line "why", difficulty, confusable-pair tag) | Rules differ between India, Sweden and the US/UK. Uncertainty drives missorting (WRAP) |
| Content | Bin scheme fixed: drop "recyclable", add residual; India mode with wet/dry/sanitary/special care | Tissues and window glass currently have no correct bin |
| Content | 40–60 items, focused on high-error ones (drinking glass, pouches, tubes, cartons, pizza boxes) | Mastered patterns become boring (Koster); target real confusion |
| Core loop | Bag randomizer that covers every bin, easy-to-hard order with breathers | Tetris 7-bag; Candy Crush staircase |
| Feedback | Response under 100 ms, moderate juice, success-dependent sound and particles, gentle wrong-answer state | Swink; Kao 2020 inverted U; CHI 2024 |
| Feedback | "Why" card after every answer, correct bin shown on wrong answers | Hattie d = 0.48; UBC 69→84% |
| Learning | Leitner, then HLR, scheduling; interleaved confusable pairs; mistake-review mode; mastery-gated unlocks | Cepeda; Settles; Brunmair; Kulik |
| Integration | Score as kg diverted or bale purity; contamination as the fail state | Zombie Division, about 7× voluntary play |
| Progression | Combos, personal bests, per-category accuracy, visible locks, forgiving weekly streak, cooperative goals | Hodent; Duolingo A/B; Waste Game backfire |
| Avoid | Hearts/lives, punishing daily streaks, global leaderboards, share-to-unlock, XP for grinding | Zagal dark patterns; L@S 2022 |
| Onboarding | Round 1 as a no-penalty tutorial with highlighted bin; two-word instructions | Hodent; WarioWare |
| Accessibility | Icon + label + position per bin; non-colour feedback; keyboard/tap input; no default timer; alt text | GAG; XAG 103 |
| Real-world bridge | "Which bin?" lookup, local cheat-sheet, positive peer norms, optional real-world missions | Fogg; Varotto & Spagnolli |
| Tech | Python 3, pure `core/`, scenes, platform layer, versioned save schema, i18n string files | PEP 373; Nystrom |
| Testing | pytest on core and content schema, headless scene tests, bot playtests, CI with web build | pygame dummy driver |
| Analytics | Anonymous session events, aggregates only, cookieless page analytics, A/B by session | COPPA 2025 rule; Plausible |
| Distribution | pygbag → itch.io + GitHub Pages; README with screenshots, how to play, sources for rules; CREDITS/licences | itch.io HTML5 docs; Kenney CC0 |
| Evaluation | Pre, post and 3-week delayed tests on unseen items; observed playtests with 5–10 first-time players | Waste Game RCT; LM-GM |

## Phased roadmap for upasanasen/Game

| Phase | Scope | Exit criteria |
|---|---|---|
| **0. Foundations (days)** | Port to Python 3. Move items to `items.json`. Replace the bins with a coherent scheme (e.g. Dry-plastic, Dry-paper/carton, Glass packaging, Wet/compost, Residual, plus India's Sanitary/Special care). Fix the tissue and window-glass answers. Add a "why" line and correct-bin reveal to every answer. Bag randomizer. pytest for scoring and content schema. Write the README | Runs on Python 3.12+. Every item has a region-valid answer and explanation. CI green |
| **1. Better terminal game (1–2 weeks)** | Textual or rich UI with icons and labels, number-key input, combo counter, per-category accuracy, personal best, mistake-review round, Leitner scheduling across sessions saved to JSON, region selector (India 2026 / Sweden / generic) | 5–10 observed playtests. Players read the "why" cards. First-attempt accuracy rises on replay |
| **2. Browser game (3–6 weeks)** | pygame-ce front end over the unchanged `core/`: drag or tap sorting, moderate juice, CC0 art and OGG audio, onboarding round, colour-blind-safe palette and high-contrast mode, no default timer. pygbag build to itch.io and GitHub Pages via CI; headless and bot tests | Response under 100 ms. Plays on desktop and mobile browsers. Bot finds no crashes in 10k sessions. Accessibility checklist passes |
| **3. Learning engine (1–2 months)** | HLR half-lives per item, interleaved confusable pairs, mastery-gated districts or materials, score reframed as bale purity or kg diverted, forgiving weekly streak, anonymous aggregate telemetry, localisation (e.g. English, Hindi, Swedish) | Delayed-test gain on unseen items is measurable. Most-confused items are identified from aggregate data |
| **4. Real-world impact (ongoing)** | "Which bin?" lookup, printable local guide, cooperative community goals, optional real-world missions, pre/post/delayed evaluation (perhaps with a school or residence). Consider Godot 4 (GDScript) if app stores or screen-reader support become priorities | Evidence of transfer beyond the game (self-report or, better, observed contamination) |

## Conclusion

The central insight is that this repo's problem is not polish. It is **what the game teaches**. A slicker version of the current quiz would teach players, more effectively, to put window glass in the glass bin, which every region researched here says is wrong. Content accuracy is therefore the first "game design" task. Region-aware data is both the fix and the product's differentiator, since established sorting games tend to assume one universal rule set.

The second insight is that the ingredients of a great game and of effective learning are largely the same components seen from two sides. Immediate, informative feedback is both "juice" and elaborated feedback. Item scheduling is both pacing and spaced repetition. Unlockable districts are both progression and mastery learning. That overlap lets a small, solo, Python-first project reach both goals without heavy machinery: a Python 3 core, a JSON rulebook, a "why" line and a scheduler go further than any engine choice. The honest limit is behaviour. Knowledge gains from games are modest and do not automatically reach the kitchen bin, so the features that make the right action easier (lookup, local guide, social norms) matter more for real impact than any leaderboard.
