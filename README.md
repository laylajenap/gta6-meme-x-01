# Me, Waiting 13 Years for GTA 6 — a make.fun meme

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for the [gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01) bounty on
[make.fun](https://make.fun) — post a GTA 6 meme on X.

## The meme

![The meme](meme.png)

GTA V came out in 2013. GTA 6 finally drops 19 November 2026 — thirteen years
later, after delay after delay, in Vice City, Leonida. The joke writes itself:
we spent over a decade waiting on a beach that never arrived. The make.fun
ghost, meanwhile, did not just wait around — it got paid. On make.fun, people
and their AI agents build things, enter paid bounties, and earn real money.
Waiting is free; winning pays.

The picture is drawn entirely in code (`generate-meme.py`, Python + PIL): a
Vice City sunset, palms, ocean, sand — with the official make.fun ghost mascot
from the [make.fun press kit](https://make.fun/press/) (`assets/mark-1024.png`)
front and centre, holding its magenta star coin.

## The post

The meme was posted on X — see `POST.json` for the post URL.

## Run

`main.ts` (Node 22, standard library only) copies `POST.json` from the
repository to the output directory:

```sh
MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

This creates `out/POST.json`. If `POST.json` cannot be copied, the program
prints an error to stderr and exits with code 1.

Regenerate the meme image with:

```sh
python3 generate-meme.py
```

## License

MIT — see [LICENSE](LICENSE).
