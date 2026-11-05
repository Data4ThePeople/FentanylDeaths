"""Turn us-atlas counties-albers-10m TopoJSON into SVG path strings for the county map.

Output data/build/geo.json:
  counties: {fips5: "M...Z"}  one path per county in a 975x610 viewBox
  states:   one path of the borders between states (arcs shared by two different states)
  nation:   the outer border
Shared borders are decoded from the same arcs, so neighbors line up exactly.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def decode_arcs(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def fmt(pts):
    out, last = [], None
    for x, y in pts:
        p = f"{x:.1f},{y:.1f}"
        if p != last:
            out.append(p)
        last = p
    return out


def ring(arcs, idxs):
    pts = []
    for i in idxs:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return "M" + "L".join(fmt(pts)) + "Z"


def polys(g):
    return g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]


def main():
    topo = json.loads((ROOT / "data/raw/geo/counties-albers-10m.json").read_text())
    arcs = decode_arcs(topo)
    counties = {}
    for g in topo["objects"]["counties"]["geometries"]:
        if g["id"] in counties:
            raise SystemExit(f"duplicate county id {g['id']}")
        counties[g["id"]] = "".join(ring(arcs, r) for p in polys(g) for r in p)

    # state borders: arcs used by two different states; nation: arcs used once
    use = {}
    for g in topo["objects"]["states"]["geometries"]:
        for p in polys(g):
            for r in p:
                for i in r:
                    use.setdefault(i if i >= 0 else ~i, set()).add(g["id"])
    inner = [i for i, s in use.items() if len(s) > 1]
    nation = [i for g in topo["objects"]["nation"]["geometries"] for p in polys(g) for r in p for i in r]
    line = lambda ids: "".join("M" + "L".join(fmt(arcs[i if i >= 0 else ~i])) for i in ids)

    out = {"counties": counties, "states": line(inner), "nation": line(nation)}
    (ROOT / "data/build").mkdir(parents=True, exist_ok=True)
    (ROOT / "data/build/geo.json").write_text(json.dumps(out, separators=(",", ":")))
    print(len(counties), "counties,", len(json.dumps(out)) // 1024, "KB of path data")


if __name__ == "__main__":
    main()
