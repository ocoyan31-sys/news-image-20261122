# The Day in One Picture — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ocoyan31-sys/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ocoyan31-sys/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

An entry for make.fun's [news-image-20261122](https://make.fun/bounty/news-image-20261122)
competition: sum up the world news of **Sunday, 22 November 2026** in one image.

## What the image shows

A front page dated in big type, with the day's most consequential stories
across regions and fields:

- **Lead story — COP31 collapses in Antalya.** The climate summit ends
  Sunday with no agreement, two days late, after the EU and vulnerable
  countries object to a final text that makes no mention of fossil fuels.
- **Iran strikes US bases in Bahrain.** Missiles and drones hit Bahrain;
  a civilian industrial facility is hit and two people are injured, and
  oil tankers are struck near the Strait of Hormuz.
- **Russian warship hit off Libya.** A suspected Ukrainian drone strike
  hits a Russian warship at Benghazi, injuring ten port workers, and a
  second Russian cargo ship burns in the Baltic.
- **Russian strike on Dymer, near Kyiv.** An apartment block partly
  collapses; rescuers search the ruins.
- **Mexico captures cartel boss "El Chapo Isidro".** Fausto Isidro Meza
  Flores is seized in Sinaloa; 11 people are killed in the raid, including
  four soldiers.
- **Factory fire in Cikande, Indonesia.** Three workers are killed and
  dozens are still missing as rescuers search the ruins.
- **Bottom row** — markets slide as the AI sell-off deepens (S&P 500
  down 3.7%, Nikkei down 5.06%); Democrats secure at least 258 US House
  seats; BepiColombo enters orbit around Mercury; Israeli settlers torch
  vehicles and homes near Ramallah; and fallout continues from the
  Shenzhen Trump-Xi-Putin summit.

## How it runs

`main.py` (Python 3.13, standard library only) draws the front page pixel by
pixel with its own small PNG writer — no network, no randomness, no image
files — and writes it to `/output/entry.png`
(or to `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader's container).
Two runs write identical bytes.

The image is a whole PNG, 1024 × 1024 pixels and under the 1 MiB cap.

## License

MIT — see [LICENSE](LICENSE).
