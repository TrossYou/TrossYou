# -*- coding: utf-8 -*-
"""portfolio/data/skills.json 에서 스킬 막대 SVG 두 장(라이트·다크)을 생성한다.
색은 portfolio/docs/design.md 의 토큰과 같다. GitHub README 는 웹폰트를 못 쓰므로 시스템 산세리프로 그린다."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.join(HERE, "..", "..", "portfolio", "data", "skills.json")
d = json.load(io.open(SKILLS, encoding="utf-8"))

THEMES = {
    "light": dict(ink="#1c1f27", muted="#5d6270", line="#e2e4ea", accent="#2e4a8b", strong="#b9c7f2"),
    "dark": dict(ink="#e9eaee", muted="#a1a5b0", line="#2a2d36", accent="#4c6cb3", strong="#3b4c86"),
}
W, ROW, GROUP_H, NAME_W, LEVEL_W, PAD = 820, 40, 34, 170, 48, 8
SANS = "IBM Plex Sans KR, Apple SD Gothic Neo, Malgun Gothic, Segoe UI, sans-serif"
MONO = "JetBrains Mono, Cascadia Mono, Consolas, monospace"

def render(theme):
    c = THEMES[theme]
    rows, y = [], 0
    last = None
    for s in d["rated"]:
        if s["group"] != last:
            y += 10 if last else 0
            rows.append(f'<text x="0" y="{y+22}" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{c["muted"]}">{s["group"].upper()}</text>')
            y += GROUP_H; last = s["group"]
        cy = y + ROW / 2
        rows.append(f'<text x="0" y="{cy+5}" font-family="{SANS}" font-size="15" font-weight="600" fill="{c["ink"]}">{s["name"]}</text>')
        bar_x, bar_w = NAME_W, W - NAME_W - LEVEL_W - PAD
        seg = (bar_w - 4 * 6) / 5
        for i in range(5):
            on = i < s["level"]
            fill = (c["accent"] if s["level"] >= 4 else c["strong"]) if on else c["line"]
            rows.append(f'<rect x="{bar_x + i*(seg+6):.1f}" y="{cy-5}" width="{seg:.1f}" height="10" rx="3" fill="{fill}"/>')
        rows.append(f'<text x="{W}" y="{cy+5}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{c["muted"]}">{s["level"]}/5</text>')
        y += ROW
    y += 14
    rows.append(f'<text x="0" y="{y+14}" font-family="{SANS}" font-size="13" fill="{c["muted"]}">써 본 것: {" · ".join(d["used"])}</text>')
    y += 34
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {y}" width="{W}" height="{y}" role="img" aria-label="스킬 별점">\n' + "\n".join(rows) + "\n</svg>\n"

for t in THEMES:
    p = os.path.join(HERE, f"skills-{t}.svg")
    io.open(p, "w", encoding="utf-8", newline="\n").write(render(t))
    print("wrote", os.path.basename(p))
