# Sorting Shift

A waste-sorting game with real recycling rules for ten countries.

You run the sorting line at a recycling centre. Items come down the belt and you drag each one into the right bin. Sort it right and the bale stays clean. Sort it wrong and you contaminate the load. Every answer comes with a one-line reason, so you learn the rule and not just the item.

**Play it:** https://upasanasen.github.io/Game/

## How to play

1. Pick a country. Each one uses its own real bins.
2. Drag the item into a bin, tap a bin, or press its number key. There is no timer.
3. Read the reason, then press **Next item**.
4. After 10 items you get a shift report with your accuracy, kg kept from landfill and bale purity.
5. Press **Review mistakes** to replay the items you got wrong without hints.

The first item of every shift is a training round: the right bin is lit and a wrong answer doesn't count. Items you get wrong come back sooner in later shifts. Progress is saved in your browser only.

## Countries

| Country | Bins | Based on |
|---|---|---|
| Canada | 5 | Toronto (Ontario Blue Box, 2026) |
| Denmark | 9 | National 10-fraction sorting system |
| Finland | 9 | Helsinki region (HSY) |
| France | 7 | Citeo packaging rules (2023) and biowaste sorting (2024) |
| India | 4 | Solid Waste Management Rules 2026 |
| Italy | 8 | National guidance, Milan and Rome |
| Norway | 7 | National rules and Sortere.no |
| Spain | 7 | Ley 7/2022 and Ecoembes |
| Sweden | 7 | Common municipal guidance |
| USA | 6 | EPA guidance and typical curbside programmes |

Rules differ between towns inside most countries. Items marked **varies locally** accept more than one bin. Always check your own municipality.

## Design choices

- **Accuracy first.** Each country's answers were researched separately with official sources, listed in the `sources` field of each file in `data/regions/`.
- **Explain every answer.** Feedback that says *why* teaches more than right/wrong alone.
- **Show the consequence.** A wrong item lands in the wrong bin, dirties the bale, then hops to the right one.
- **Accessible bins.** Every bin has a colour, a pattern, an icon and a name, so nothing depends on colour alone. Keyboard play works, and the game respects "reduce motion".
- **No dark patterns.** No lives, no punishing streaks, no global leaderboards.

The research behind these choices is in [docs/research/Building a great sorting game.md](docs/research/Building%20a%20great%20sorting%20game.md).

## Project layout

```
index.html            The whole game: one file, no build step needed to play
data/regions/*.json   Bins, answers and reasons for each country
tools/build_regions.py  Copies the country files into index.html
docs/research/        Design research report
legacy/game.py        The original 2020 terminal quiz (Python 2)
```

## Adding or fixing a country

1. Edit or add a file in `data/regions/`. Each item has `a` (accepted bin ids, main answer first), `w` (the one-line reason) and `v` (true if it varies locally).
2. Optionally give the bins a short label and icon in `OVERRIDES` in `tools/build_regions.py`.
3. Run:

```bash
python3 tools/build_regions.py
```

4. Open `index.html` in a browser to test.

## Roadmap

- **Where did it go?** After each shift, follow the truck and see each bale's fate and its carbon cost or saving.
- **Level 2, Driver:** plan collection routes.
- **Level 3, Plant manager:** send bales to recycling, compost, energy or landfill, with carbon (and later water) footprints.
- **Level 4, Designer:** redesign products and packaging so they are easier to recycle.

## Licence

MIT. See [LICENSE](LICENSE).
