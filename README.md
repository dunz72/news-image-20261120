[![make.fun bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dunz72/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dunz72/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World in One Day — Friday 20 November 2026

A single 1024×1024 front page that sums up Friday 20 November 2026 in 45
stories across 6 continents: three hero stories, ten feature cards, a world
map with numbered pins, and a two-column day-in-brief list.

The page is drawn entirely in code — every panel, skyline, bridge, chart,
globe, dove, ship, flag and continent is an original vector illustration
rendered with Pillow. No photographs, no stock art, no official logos.

## The front page

- **Masthead** — "THE DAY IN WORLD NEWS", Friday 20 November 2026.
- **Hero 1 — GTA VI: $2.36bn in a day.** A sunset city skyline: an orange
  sun over dark towers, a glowing neon sign, two evening figures and a red
  car on the boulevard. Sensor Tower estimates 24.58m copies sold on day
  one — the biggest entertainment launch ever.
- **Hero 2 — Kyiv hit, 8 dead.** A cable bridge at night under a pale moon,
  lit by two starburst blasts. Russia's overnight barrage hit bridges,
  energy and ports; a cargo ship bound for Odesa was struck.
- **Hero 3 — Wall St's worst week.** Falling red candlesticks and a
  downtrend line over a dark trading screen: the Dow plunged 1,101 points
  below 50,000 and the Nikkei tumbled 5%.
- **Ten features** — COP31, Anthropic's IPO, Nvidia, Cyclone Akvan, Gaza,
  the Houthi missile on Riyadh, Prabowo and Xi, Estonia's border shutdown,
  Voyager 1 and the wet Las Vegas FP2.
- **Where it happened** — a world map with numbered pins 1–13 and a
  continent legend.
- **The day in brief** — stories 14–45 in two numbered columns.

## Run it

Requires Python 3 and Pillow:

```sh
pip install pillow
python3 main.py
```

By default the program writes `/output/entry.png` (the harness directory).
To write next to the script instead:

```sh
MAKEFUN_OUTPUT_DIR=. python3 main.py
```

The render is fully deterministic: two runs produce byte-identical PNGs.

## The 45 stories

### Heroes

1. **GTA VI: $2.36bn in a day** (Culture · Leonida) — Sensor Tower
   estimates 24.58m copies sold on day one, biggest entertainment launch
   ever; Metacritic 99, PlayStation Store 4.86/5.
2. **Kyiv hit, 8 dead** (War in Ukraine · Kyiv) — Russia's overnight
   barrage hits bridges, energy and ports; a cargo ship bound for Odesa
   is struck. France calls for a UN Security Council meeting.
3. **Wall St's worst week** (Markets · New York) — Dow plunges 1,101
   points below 50,000; S&P falls a sixth straight day as Anthropic's
   $81bn debut fails to lift AI shares. Nikkei tumbles 5%.

### Features

4. **COP31 draft erases fossil fuels** (Climate) — Final-day text drops
   every mention of oil, gas and coal; talks head for overtime.
5. **Anthropic slips on day two** (AI IPO) — ANT opened at $111.50,
   closed $97.17 — still +17% on its $83 IPO price.
6. **Nvidia in turmoil** (Tech) — H200 chip shipments to China halted;
   board refuses to bring back ousted Huang.
7. **Cyclone Akvan makes landfall** (Weather) — Storm crosses near
   Gopalpur at 70-80 km/h; 300,000 evacuated, no major damage.
8. **Gaza plan scores 4 of 26** (Gaza) — Board of Peace warns the
   ceasefire risks collapse; Israel controls 70% of Gaza.
9. **Houthi missile hits Riyadh** (Middle East) — Blast damages a
   sovereign wealth fund tower; Houthis threaten Red Sea ports.
10. **Prabowo and Xi talk seas** (Asia) — South China Sea joint
    development agreed; 35 deals worth $15bn signed.
11. **Estonia shuts Russia border** (Europe) — Crossings close from
    1 December for six months; Moscow cries 'Iron Curtain'.
12. **Voyager 1, one light-day out** (Space) — Probe crosses 26bn km —
    but its data stopped on 14 November. BepiColombo reaches Mercury.
13. **Russell tops wet Vegas FP2** (Sport) — Mercedes star clocks
    1:47.272; Gasly +0.071, Leclerc third. FP1 washed out.

### The day in brief

14. Myanmar calls ICJ genocide ruling 'unfair'
15. Russia rejects NATO-style guarantees for Ukraine
16. Moscow: Kallas role would collapse Ukraine talks
17. Iraq deploys forces in militia stronghold
18. Trump asks top court to block Venezuelan TPS
19. Supreme Court to review asylum order
20. US and Venezuela sign military cooperation deal
21. US Senate rejects Iran war-powers resolution
22. Trump warns Iran may seek chemical weapons
23. Iran war in ninth month; ADNOC ship struck
24. UK pledges 1,000+ drones for Ukraine
25. EU to summon Russian envoy over Kyiv damage
26. Poland probes unknown objects near border
27. UK-EU set to agree youth mobility scheme
28. UN secretary-general race stalls
29. Bukele registers for third term
30. Migrant boat capsizes off Senegal
31. Drone strike kills 10 at Sudan gold mine
32. Kenya discharges last Ebola patient
33. Bangladesh violence ahead of Hasina return
34. Denmark ratifies Greenland security deal
35. Colombia protests over tax plans
36. Japan inflation rises; rate hike on track
37. Philippines-Chile sign free-trade deal
38. Japan's Takaichi gets cool APEC reception
39. Spain's Sanchez admits mistakes
40. Isomorphic Labs raises $5bn Series C
41. Trump pardons Pete Rose posthumously
42. US sanctions Comancheros and 'Ndrangheta
43. Gemini agent runs Mac apps for Google
44. Meta's Muse leaks private chats
45. Moonshot cancels $150m Nvidia chip deal

## Sources

Reuters · AP · AFP · BBC · Al Jazeera · The Day in World News,
Friday 20 November 2026.

## Bounty

Built for the [news-image-20261120](https://make.fun/bounty/news-image-20261120)
bounty on make.fun — "Sum up 20 November's world news in one image".
