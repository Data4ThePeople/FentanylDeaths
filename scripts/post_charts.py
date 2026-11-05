"""Static charts for posts/fentanyl-deaths-by-county, drawn from the same data the post's numbers use:
data/build/dashboard.json (fentanyl = multiple cause T40.4) and, for chart 1, SUD_V3's WONDER exports of all
drug overdose deaths (underlying cause X40-X44, X60-X64, X85, Y10-Y14) summed over states, as in
scripts/story_numbers.py.

House style: dark surface #181A1B, ink #BBBDC0, every chart titled, legends as colored words,
declines as leftward bars. Nothing hardcoded: every value and label is computed here.

Run: python scripts/post_charts.py   -> posts/fentanyl-deaths-by-county/images/0N-*.png
"""
import csv, io, json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "posts/fentanyl-deaths-by-county/images"
SUD = ROOT.parent / "SUD_V3/data/raw/wonder"
D = json.loads((ROOT / "data/build/dashboard.json").read_text())
Y = D["years"]
ix = Y.index

SURFACE, INK, INK_DIM, MUTED, GRID = "#181A1B", "#BBBDC0", "#8A9098", "#6B7178", "#2A2D2F"
BLUE, YELLOW, MAGENTA = "#3987e5", "#c98500", "#d55181"  # the validated dark trio (GwinnettCounty plot_style)
CREDIT = "Built by Data 4 The People"
SRC = "Source: CDC WONDER, Multiple Cause of Death, 1999-2020 and 2018-2024 Single Race."
FEN_NOTE = "Fentanyl deaths: overdose deaths involving synthetic opioids other than methadone (T40.4)."

mpl.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK_DIM, "ytick.color": INK_DIM,
    "axes.edgecolor": GRID, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11, "text.parse_math": False, "figure.dpi": 160, "savefig.dpi": 160,
})
comma = FuncFormatter(lambda v, _: f"{v:,.0f}")


def titleblock(fig, title, subtitle, y=0.975):
    fig.text(0.03, y, title, color=INK, fontsize=17, fontweight="bold", va="top", ha="left")
    fig.text(0.03, y - 0.36 / fig.get_figheight(), subtitle, color=INK_DIM, fontsize=11, va="top", ha="left",
             linespacing=1.45)


def credit(fig, source):
    fig.text(0.03, 0.015, source, color=MUTED, fontsize=8.5, ha="left", va="bottom", linespacing=1.4)
    fig.text(0.97, 0.015, CREDIT, color=MUTED, fontsize=8.5, ha="right", va="bottom")


def words(fig, x, y, parts):
    """Legend as colored words, laid left to right."""
    r = fig.canvas.get_renderer()
    for text, color in parts:
        t = fig.text(x, y, text, color=color, fontsize=11, fontweight="bold" if color != INK_DIM else "normal",
                     va="top", ha="left")
        x += t.get_window_extent(r).width / fig.bbox.width


def rows(p):
    L = Path(p).read_text().split("\n")
    end = next((i for i, l in enumerate(L) if l.startswith('"---"')), len(L))
    return [r for r in csv.DictReader(io.StringIO("\n".join(L[:end]))) if not r.get("Notes")]


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name)
    plt.close(fig)
    print("wrote", OUT / name)


C = {f: g for f, g in D["counties"].items() if f in D["paths"]}


def pub(g, y, m=20):
    i = ix(y)
    return g["s"][i] == "P" and g["d"][i] is not None and g["d"][i] >= m


# ---- 01: all overdose deaths vs deaths involving fentanyl
def chart_overdose():
    tot = Counter()
    for p, lo, hi in ((SUD / "ucd_1999_2020_state_year_drug.csv", 1999, 2017),
                      (SUD / "ucd_2018_2024_state_year_drug.csv", 2018, 2024)):
        for r in rows(p):
            if lo <= int(r["Year"]) <= hi:
                tot[int(r["Year"])] += int(r["Deaths"])
    fen = dict(zip(Y, D["us"]["d"]))
    yrs = sorted(tot)
    assert yrs == list(range(2001, Y[-1] + 1)), "overdose export should cover 2001 to the last map year"
    fig, ax = plt.subplots(figsize=(10, 6.2))
    fig.subplots_adjust(left=0.09, right=0.88, top=0.76, bottom=0.12)
    # Two published series drawn as overlapping areas: all overdose deaths behind, deaths involving fentanyl
    # in front. The yellow band left showing is overdose deaths without fentanyl; nothing is subtracted.
    T, F = [tot[y] for y in yrs], [fen[y] for y in yrs]
    ax.fill_between(yrs, 0, T, color=YELLOW, lw=0)
    ax.fill_between(yrs, 0, F, color=BLUE, lw=0)
    ax.plot(yrs, F, color=SURFACE, lw=2)          # 2px surface gap between the two fills
    for y in (2013, 2022, 2024):
        for s, c in ((tot, YELLOW), (fen, BLUE)):
            ax.plot(y, s[y], "o", ms=6, color=INK, mec=SURFACE, mew=2)
            last = y == yrs[-1]
            ax.annotate(f"{s[y]:,}", (y, s[y]), xytext=(8, 0) if last else (0, 9), textcoords="offset points",
                        ha="left" if last else "center", va="center" if last else "bottom", fontsize=9.5,
                        color=INK, bbox=dict(boxstyle="round,pad=0.2", fc=SURFACE, ec="none", alpha=0.85))
    ax.set_ylim(0, max(tot.values()) * 1.12)
    ax.set_xlim(yrs[0] - 0.5, yrs[-1] + 0.5)
    ax.yaxis.set_major_formatter(comma)
    ax.grid(axis="y"); ax.set_axisbelow(True); ax.tick_params(length=0); ax.spines["left"].set_visible(False)
    ax.set_xticks(range(yrs[0], yrs[-1] + 1, 3))
    titleblock(fig, "Fentanyl drove the rise in overdose deaths",
               f"Overdose deaths per year in the U.S., {yrs[0]} to {yrs[-1]}. The top edge is all overdose deaths.")
    words(fig, 0.03, 0.855, [("Deaths involving fentanyl", BLUE), ("   and   ", INK),
                              ("overdose deaths without fentanyl", YELLOW)])
    credit(fig, SRC + "\n" + FEN_NOTE + " All overdose deaths: state totals summed.")
    save(fig, "01-overdose-vs-fentanyl.png")


# ---- 02: the 2006 outbreak in Cook County and Wayne County
def chart_2006():
    want = {"Cook County, IL": "Cook County, Illinois (Chicago)", "Wayne County, MI": "Wayne County, Michigan (Detroit)"}
    yrs = [y for y in Y if y <= 2012]
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.12, hspace=0.45)
    top = max(g["d"][ix(y)] or 0 for g in C.values() if g["n"] in want for y in yrs)
    for ax, (key, label) in zip(axes, want.items()):
        g = next(g for g in C.values() if g["n"] == key)
        for y in yrs:
            d, s = g["d"][ix(y)], g["s"][ix(y)]
            if s == "P" and d is not None:
                ax.bar(y, d, width=0.7, color=BLUE)
                ax.text(y, d + top * 0.03, f"{d:,}", ha="center", va="bottom", fontsize=9.5, color=INK)
            else:
                ax.text(y, top * 0.03, "0-9", ha="center", va="bottom", fontsize=8.5, color=MUTED)
        ax.set_title(label, loc="left", fontsize=12, color=INK, pad=6)
        ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.tick_params(length=0)
    axes[0].set_ylim(0, top * 1.18)
    axes[1].set_xticks(yrs)
    axes[1].tick_params(axis="x", labelsize=9.5)
    titleblock(fig, "Fentanyl deaths spiked in Chicago and Detroit in 2006",
               "Fentanyl deaths per year by county of residence, 1999 to 2012. "
               "\"0-9\" means CDC does not publish the count.")
    credit(fig, SRC + "\n" + FEN_NOTE)
    save(fig, "02-outbreak-2006.png")


# ---- 03: highest rate in any year, counties with 20+ deaths
def chart_peaks(n=10):
    peaks = sorted(((max((C[f]["r"][ix(y)], y) for y in Y if pub(C[f], y)), f)
                    for f in C if any(pub(C[f], y) for y in Y)), reverse=True)[:n]
    fig, ax = plt.subplots(figsize=(10, 6.6))
    fig.subplots_adjust(left=0.36, right=0.93, top=0.80, bottom=0.13)
    labels = []
    for k, ((r, y), f) in enumerate(peaks):
        g = C[f]
        ax.barh(k, r, height=0.68, color=BLUE if g["n"].endswith(", WV") else INK_DIM)
        ax.text(r + 2, k, f"{r:.1f}", va="center", fontsize=10, color=INK)
        labels.append(f"{g['n']}  {y}")
    ax.set_yticks(range(len(peaks)), labels, fontsize=10.5, color=INK)
    ax.invert_yaxis()
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    ax.set_xlim(0, peaks[0][0][0] * 1.1)
    titleblock(fig, "West Virginia holds the highest county rates on record",
               "Each county's highest fentanyl death rate in any year, per 100,000 residents, 1999 to 2024")
    words(fig, 0.03, 0.855, [("West Virginia", BLUE), ("   and   ", INK), ("other states", INK_DIM)])
    credit(fig, SRC + "\n" + FEN_NOTE + "\nCounties with 20 or more deaths in that year only.")
    save(fig, "04-highest-county-rates.png")


# ---- 04: state change 2023 to 2024
def chart_states():
    a, b = ix(2023), ix(2024)
    st = sorted((((g["d"][b] - g["d"][a]) / g["d"][a] * 100, g["n"], None) for g in D["states"].values()
                 if g["d"][a] and g["d"][b]), reverse=True)
    missing = sorted(g["n"] for g in D["states"].values() if not (g["d"][a] and g["d"][b]))
    fig, ax = plt.subplots(figsize=(10, 13))
    fig.subplots_adjust(left=0.24, right=0.95, top=0.905, bottom=0.06)
    lo = min(p for p, _, _ in st)
    for k, (p, n, w) in enumerate(st):
        ax.barh(k, p, height=0.7, color=BLUE)
        ax.text(p - 0.8, k, f"{p:.1f}%", va="center", ha="right", fontsize=9, color=INK)
    ax.set_yticks(range(len(st)), [n for _, n, _ in st], fontsize=9.5, color=INK)
    ax.yaxis.tick_right(); ax.tick_params(axis="y", pad=4)
    ax.set_yticks(range(len(st)))
    ax.set_yticklabels([n for _, n, _ in st])
    ax.set_ylim(len(st) - 0.4, -0.6)
    ax.set_xlim(lo * 1.18, 0)
    ax.axvline(0, color=INK_DIM, lw=0.8)
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    fig.subplots_adjust(left=0.05, right=0.80, top=0.93, bottom=0.07)
    titleblock(fig, "Fentanyl deaths fell in every state with data for both years",
               "Change in fentanyl deaths from 2023 to 2024", y=0.985)
    credit(fig, SRC + "\n" + FEN_NOTE + "\nNot shown, to protect small county counts: "
           + ", ".join(missing) + ".")
    save(fig, "05-state-change-2024.png")


# ---- 05: counties with more deaths in 2024
def chart_rose():
    a, b = ix(2023), ix(2024)
    up = [C[f] for f in C if pub(C[f], 2023) and pub(C[f], 2024) and C[f]["d"][b] > C[f]["d"][a]]
    up.sort(key=lambda g: -(g["d"][b] - g["d"][a]) / g["d"][a])
    fig, ax = plt.subplots(figsize=(10, 9))
    fig.subplots_adjust(left=0.36, right=0.82, top=0.89, bottom=0.10)
    hi = max((g["d"][b] - g["d"][a]) / g["d"][a] * 100 for g in up)
    for k, g in enumerate(up):
        p = (g["d"][b] - g["d"][a]) / g["d"][a] * 100
        ax.barh(k, p, height=0.68, color=BLUE)
        ax.text(p + hi * 0.015, k, f"+{p:.1f}%   ({g['d'][a]:,} to {g['d'][b]:,})", va="center", fontsize=9.5,
                color=INK)
    ax.set_yticks(range(len(up)), [g["n"] for g in up], fontsize=10, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, hi)
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    titleblock(fig, f"{len(up)} counties had more fentanyl deaths in 2024",
               "Change in fentanyl deaths from 2023 to 2024, deaths in parentheses", y=0.98)
    credit(fig, SRC + "\n" + FEN_NOTE + "\nCounties with 20 or more deaths in both years.")
    save(fig, "06-counties-rose-2024.png")


# ---- 06: CDC's three waves, drawn on death rates by opioid type
def chart_waves():
    """Crude death rates per 100,000 for overdose deaths involving each opioid type (multiple cause), same
    year split as chart 1: 1999-2020 export through 2017, 2018-2024 export after. Fentanyl comes from the map's
    own U.S. series so it matches the post. Wave start years are CDC's (understanding-the-opioid-overdose-epidemic)."""
    kinds = {"T40.2": ("Prescription opioids", YELLOW), "T40.1": ("Heroin", MAGENTA)}
    R = {k: {} for k in kinds}
    for p, lo, hi in ((SUD / "mcd_1999_2020_year_drugtype.csv", 1999, 2017),
                      (SUD / "mcd_2018_2024_year_drugtype.csv", 2018, 2024)):
        for r in rows(p):
            code = r["Multiple Cause of death Code"]
            if code in kinds and lo <= int(r["Year"]) <= hi:
                assert int(r["Year"]) not in R[code], "duplicate year"
                R[code][int(r["Year"])] = float(r["Crude Rate"])
    fen = {y: r for y, r in zip(Y, D["us"]["r"])}
    yrs = sorted(R["T40.2"])
    assert all(sorted(R[k]) == yrs for k in R) and yrs == list(range(2001, Y[-1] + 1))
    series = [(R["T40.2"], *kinds["T40.2"]), (R["T40.1"], *kinds["T40.1"]), (fen, "Fentanyl", BLUE)]

    fig = plt.figure(figsize=(10, 7.6))
    band = fig.add_axes([0.07, 0.68, 0.78, 0.15], sharex=None)
    ax = fig.add_axes([0.07, 0.11, 0.78, 0.54])
    x0, x1 = yrs[0] - 0.5, yrs[-1] + 0.5
    waves = [(x0, 2010, YELLOW), (2010, 2013, MAGENTA), (2013, x1, BLUE)]
    for a, b, c in waves:
        band.fill_between([a + 0.06, b - 0.06], 0, 0.08, color=c, lw=0)
    band.text(x0 + 0.1, 0.42, "Wave 1: prescription opioids", color=INK, fontsize=11.5, fontweight="bold")
    band.text(x0 + 0.1, 0.36, "Began in the 1990s with more prescribing", color=INK_DIM, fontsize=9.5, va="top")
    band.text(2013.1, 0.42, "Wave 3: synthetic opioids", color=INK, fontsize=11.5, fontweight="bold")
    band.text(2013.1, 0.36, "Began in 2013, \"particularly\" illegally made fentanyl", color=INK_DIM, fontsize=9.5,
              va="top")
    band.text(2011.5, 0.86, "Wave 2: heroin", color=INK, fontsize=11.5, fontweight="bold", ha="center")
    band.text(2011.5, 0.80, "Began in 2010", color=INK_DIM, fontsize=9.5, ha="center", va="top")
    band.plot([2011.5, 2011.5], [0.1, 0.6], color=INK_DIM, lw=0.8)
    band.set_xlim(x0, x1); band.set_ylim(0, 1); band.axis("off")

    for yv in (2010, 2013):
        ax.axvline(yv, color=INK_DIM, lw=0.8, ls=(0, (3, 3)))
    for S, name, c in series:
        ax.plot(yrs, [S[y] for y in yrs], color=c, lw=2.2)
        ax.text(yrs[-1] + 0.4, S[yrs[-1]], name, color=c, fontsize=10.5, fontweight="bold", va="center")
    for y in (2013, 2022):
        ax.plot(y, fen[y], "o", ms=6, color=INK, mec=SURFACE, mew=2)
        ax.annotate(f"{fen[y]:.1f}", (y, fen[y]), xytext=(-8, 6), textcoords="offset points", ha="right",
                    fontsize=10, color=INK)
    ax.annotate("2014 to 2015: up 72%, \"likely driven primarily\nby illicitly manufactured fentanyl\" (CDC)",
                ((2014 + 2015) / 2, (fen[2014] + fen[2015]) / 2), xytext=(2002.5, 8), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK_DIM, lw=0.8))
    ax.set_xlim(x0, x1)
    ax.set_ylim(0, max(fen.values()) * 1.1)
    ax.grid(axis="y"); ax.set_axisbelow(True); ax.tick_params(length=0); ax.spines["left"].set_visible(False)
    ax.set_xticks(range(yrs[0], yrs[-1] + 1, 3))
    ax.set_ylabel("Deaths per 100,000 people", color=INK_DIM, fontsize=10)
    titleblock(fig, "The three waves of the opioid crisis",
               f"U.S. overdose death rate by type of opioid involved, {yrs[0]} to {yrs[-1]}. Waves as CDC describes them.",
               y=0.975)
    credit(fig, SRC + "\nPrescription opioids: natural and semisynthetic opioids (T40.2), such as oxycodone. Heroin: T40.1. "
                "Fentanyl: T40.4.\nA death can involve more than one type. The 72% is CDC's figure (age-adjusted rate, MMWR 2016).")
    save(fig, "03-three-waves.png")


if __name__ == "__main__":
    chart_overdose()
    chart_2006()
    chart_peaks()
    chart_states()
    chart_rose()
    chart_waves()
