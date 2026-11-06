"""Hero image: a 3D ball-and-stick model of fentanyl, drawn from PubChem's 3D conformer (CID 3345).

Source: https://pubchem.ncbi.nlm.nih.gov/compound/3345 (3D SDF saved in data/raw/hero/).
Renders with a numpy z-buffer (spheres for atoms, sphere chains for bonds), 2x supersampled,
then downsampled to 1680x1080. House colors: background #181A1B, carbon ink gray, nitrogen blue,
oxygen magenta, hydrogen dim.

Run: python3 scripts/hero_molecule.py
Writes posts/fentanyl-deaths-by-county/images/fentanyl-deaths-by-county-hero-source.png (the
render) and the 1680x1080 hero beside it.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SDF = ROOT / "data/raw/hero/fentanyl-cid3345-3d.sdf"
IMG = ROOT / "posts/fentanyl-deaths-by-county/images"
W, H, SS = 1680, 1080, 2
BG = np.array([0x18, 0x1A, 0x1B]) / 255

COLOR = {"C": "#BBBDC0", "N": "#3987e5", "O": "#d55181", "H": "#6B7178"}
RADIUS = {"C": 0.42, "N": 0.44, "O": 0.44, "H": 0.24}
BOND_R = 0.13


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255


def read_sdf(p):
    L = p.read_text().splitlines()
    na, nb = int(L[3][:3]), int(L[3][3:6])
    atoms = [(l.split()[3], np.array(list(map(float, l.split()[:3])))) for l in L[4:4 + na]]
    bonds = [(int(l[:3]) - 1, int(l[3:6]) - 1) for l in L[4 + na:4 + na + nb]]
    return atoms, bonds


def rotation(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def main():
    atoms, bonds = read_sdf(SDF)
    el = [a[0] for a in atoms]
    xyz = np.array([a[1] for a in atoms])
    xyz -= xyz.mean(axis=0)
    # orient: longest extent along x, then a tilt so rings read in depth
    _, _, vt = np.linalg.svd(xyz)
    xyz = xyz @ vt.T
    xyz = xyz @ rotation(np.radians(-20), np.radians(38), np.radians(-8)).T

    w, h = W * SS, H * SS
    span = max(np.ptp(xyz[:, 0]) / (w * 0.80), np.ptp(xyz[:, 1]) / (h * 0.78))
    scale = 1 / span
    cx = (xyz[:, 0].max() + xyz[:, 0].min()) / 2
    cy = (xyz[:, 1].max() + xyz[:, 1].min()) / 2

    zbuf = np.full((h, w), -np.inf)
    rgb = np.tile(BG, (h, w, 1))
    light = np.array([-0.45, 0.55, 0.70]); light /= np.linalg.norm(light)

    def sphere(p, r, color):
        sx = (p[0] - cx) * scale + w / 2
        sy = h / 2 - (p[1] - cy) * scale
        rp = r * scale
        x0, x1 = int(max(sx - rp, 0)), int(min(sx + rp + 1, w))
        y0, y1 = int(max(sy - rp, 0)), int(min(sy + rp + 1, h))
        if x0 >= x1 or y0 >= y1:
            return
        X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        dx, dy = (X - sx) / rp, (sy - Y) / rp
        d2 = dx ** 2 + dy ** 2
        m = d2 <= 1
        dz = np.sqrt(np.clip(1 - d2, 0, 1))
        z = p[2] * scale + dz * rp
        zb = zbuf[y0:y1, x0:x1]
        m &= z > zb
        if not m.any():
            return
        n = np.stack([dx, dy, dz], -1)
        diff = np.clip(n @ light, 0, 1)
        spec = np.clip(n @ (light + np.array([0, 0, 1])) / np.linalg.norm(light + np.array([0, 0, 1])), 0, 1) ** 40
        rim = (1 - dz) ** 3
        shade = (0.28 + 0.72 * diff)[..., None] * color + 0.35 * spec[..., None] - 0.18 * rim[..., None] * color
        zb[m] = z[m]
        rgb[y0:y1, x0:x1][m] = np.clip(shade, 0, 1)[m]

    # bonds first is unnecessary with a z-buffer; draw them as dense sphere chains, colored half and half
    for i, j in bonds:
        a, b = xyz[i], xyz[j]
        n = max(int(np.linalg.norm(b - a) * scale / (BOND_R * scale * 0.08)), 2)
        for k in range(n + 1):
            t = k / n
            sphere(a + (b - a) * t, BOND_R, hexrgb(COLOR[el[i] if t < 0.5 else el[j]]) * 0.85)
    for e, p in zip(el, xyz):
        sphere(p, RADIUS[e], hexrgb(COLOR[e]))

    # depth cue: fade far parts slightly toward the background
    zn = np.where(np.isfinite(zbuf), zbuf, np.nan)
    lo, hi = np.nanmin(zn), np.nanmax(zn)
    fog = np.where(np.isfinite(zbuf), 0.30 * (hi - zbuf) / (hi - lo), 0)[..., None]
    rgb = rgb * (1 - fog) + BG * fog

    im = Image.fromarray((rgb * 255).round().astype(np.uint8)).resize((W, H), Image.LANCZOS)
    src = IMG / "fentanyl-deaths-by-county-hero-source.png"
    im.save(src)
    im.save(IMG / "fentanyl-deaths-by-county-hero-1680x1080.png")
    print("wrote", src, im.size)


if __name__ == "__main__":
    main()
