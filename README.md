# The World in One Page — Saturday 21 November 2026

A one-page newspaper front page summing up the world news of Saturday
21 November 2026, drawn programmatically with Pillow. Entry for
[news-image-20261121](https://make.fun/bounty/news-image-20261121) on make.fun.

## Stories on the page

- **Lead — Poland / NATO:** Russian missiles land in Poland; Warsaw calls it
  a deliberate provocation, NATO condemns a grave violation of allied airspace.
- **Shenzhen — Summit:** Trump, Xi and Putin hold their first trilateral
  summit and leave with little agreed.
- **New York — Markets:** the S&P 500 slides into correction as AI stocks plunge.
- **New York — Justice:** Nikhil Gupta sentenced to 19½ years over a
  murder-for-hire plot against a Sikh separatist leader.
- **Brussels — Europe:** the UK and EU sign deals on food, carbon markets and
  youth mobility.
- **Science:** an Anthropic researcher says Claude proved the Riemann Hypothesis.
- **Ticker:** Kyiv bridges hit, Denmark accuses Russian agents, COP31
  deadlocked, arson in Bangladesh.

## How it is built

`build_image.py` draws the page with Pillow (DejaVu fonts, fixed palette,
fixed layout — no network, no clock, no randomness). Run it twice and the
bytes are identical:

```sh
python3 build_image.py entry.png
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The image is 1024×1024, ~138 KB, within the
1 MiB limit.

## License

MIT — see `LICENSE`.
