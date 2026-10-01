# -*- coding: utf-8 -*-
"""프로필 README 의 SVG 를 디자인 시스템 토큰으로 생성한다.
hero · about · timeline · skills, 각각 라이트·다크. 데이터는 portfolio/data/ 에서 읽는다.
GitHub 는 웹폰트를 못 쓰므로 시스템 산세리프로 그린다. 글자 폭은 어림잡아 여유를 둔다."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "portfolio", "data")
skills = json.load(io.open(os.path.join(DATA, "skills.json"), encoding="utf-8"))
timeline = json.load(io.open(os.path.join(DATA, "timeline.json"), encoding="utf-8"))

T = {
    "light": dict(ground="#fafafa", surface="#ffffff", tint="#e7ecfa", strong="#b9c7f2", ink="#1c1f27", muted="#5d6270", line="#e2e4ea", accent="#2e4a8b", atext="#2e4a8b", on="#ffffff"),
    "dark": dict(ground="#0f1114", surface="#17191f", tint="#1f2744", strong="#3b4c86", ink="#e9eaee", muted="#a1a5b0", line="#2a2d36", accent="#4c6cb3", atext="#9db1ec", on="#ffffff"),
}
W = 820
SANS = "IBM Plex Sans KR, Apple SD Gothic Neo, Malgun Gothic, Segoe UI, sans-serif"
MONO = "JetBrains Mono, Cascadia Mono, Consolas, monospace"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, size, fill, weight=400, family=SANS, anchor="start", spacing=None):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{sp}>{esc(s)}</text>'

def width_of(s, size):
    # 한글 0.95em, 그 외 0.55em 어림
    return sum(size * (0.95 if ord(ch) > 0x2E80 else 0.55) for ch in s)

def svg(h, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{esc(label)}">\n' + "\n".join(body) + "\n</svg>\n"

# ------------------------------------------------------------------ hero
def hero(c):
    b = []
    # 아이브로우: 짧은 선 + 영문 대문자 mono
    b.append(f'<rect x="0" y="22" width="24" height="2" fill="{c["accent"]}"/>')
    b.append(text(34, 27, "FRONTEND DEVELOPER", 12, c["muted"], 500, MONO, spacing="1.6"))
    # 이름
    b.append(text(0, 84, "유승주", 48, c["ink"], 700))
    b.append(text(150, 84, "(TrossYou)", 22, c["muted"], 400))
    # 한 문장. 핵심 단어는 accent-text
    y = 128
    b.append(f'<text x="0" y="{y}" font-family="{SANS}" font-size="18" fill="{c["ink"]}">무엇을 결정했고, 무엇이 <tspan fill="{c["atext"]}" font-weight="600">틀렸고</tspan>, 무엇을 남겼는지</text>')
    b.append(text(0, y + 28, "적어 두는 프론트엔드 개발자입니다.", 18, c["ink"]))
    # 오른쪽 통계 타일 (surface + line, radius 14)
    tx, ty, tw, th = 560, 10, 260, 150
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}"/>')
    b.append(text(tx + 24, ty + 34, "검색 결과 서체 준비 시간", 13, c["ink"], 500))
    b.append(text(tx + 24, ty + 54, "PinLog · Chrome 성능 패널", 12, c["muted"]))
    b.append(text(tx + 24, ty + 104, "913ms", 18, c["muted"], 400, MONO))
    b.append(text(tx + 92, ty + 104, "→", 18, c["muted"], 400, MONO))
    b.append(text(tx + 118, ty + 106, "149", 36, c["atext"], 600, MONO))
    b.append(text(tx + 190, ty + 104, "ms", 18, c["muted"], 400, MONO))
    # 5칸 막대: 84% 단축을 칸으로 보여주지 않고, 그냥 리듬용 선 하나
    b.append(f'<rect x="{tx + 24}" y="{ty + 124}" width="{tw - 48}" height="4" rx="2" fill="{c["line"]}"/>')
    b.append(f'<rect x="{tx + 24}" y="{ty + 124}" width="{int((tw - 48) * 149 / 913)}" height="4" rx="2" fill="{c["accent"]}"/>')
    return svg(176, b, "유승주 (TrossYou) · 프론트엔드 개발자 · 무엇을 결정했고, 무엇이 틀렸고, 무엇을 남겼는지 적어 두는 프론트엔드 개발자입니다 · 검색 결과 서체 준비 시간 913ms → 149ms")

# ------------------------------------------------------------------ about
def about(c):
    b = []
    # 열 폭은 값 길이에 맞춘다. 네 번째 칸(위치)은 사이트 Contact 에 있으니 여기서는 뺀다
    cells = [("교육", "SSAFY 15기 · 2026.01–12", 0), ("학력", "숭실대학교 컴퓨터학부 졸업", 250), ("자격", "정보처리기사 · SQLD · TOPCIT 수준 3", 520)]
    b.append(f'<rect x="0" y="0" width="{W}" height="1" fill="{c["line"]}"/>')
    for k, v, x in cells:
        b.append(text(x, 30, k.upper(), 12, c["muted"], 500, MONO, spacing="1.2"))
        b.append(text(x, 54, v, 14, c["ink"], 500))
    b.append(f'<rect x="0" y="72" width="{W}" height="1" fill="{c["line"]}"/>')
    tiles = [("510", "/ 692", "", "프론트엔드 영역 커밋 (74%)", "FINCH · finch-frontend, 2026.09.28 기준"),
             ("149", "", "ms", "검색 결과 서체 준비 시간, 913ms에서", "PinLog · Chrome 성능 패널 측정"),
             ("105", "", "건", "파트 간 문의 정리", "FINCH 문의함 문서, 6주 누적")]
    ty, th, gap = 92, 118, 16
    tw = (W - gap * 2) / 3
    for i, (v, of, unit, label, src) in enumerate(tiles):
        x = i * (tw + gap)
        b.append(f'<rect x="{x:.0f}" y="{ty}" width="{tw:.0f}" height="{th}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}"/>')
        b.append(text(x + 20, ty + 44, v, 30, c["atext"], 600, MONO))
        vx = x + 20 + width_of(v, 30) * 1.15
        if of:
            b.append(text(vx + 4, ty + 44, of, 16, c["muted"], 400, MONO))
        if unit:
            b.append(text(vx + 2, ty + 44, unit, 16, c["muted"], 400, SANS))
        b.append(text(x + 20, ty + 72, label, 13, c["ink"]))
        b.append(text(x + 20, ty + 94, src, 11, c["muted"]))
    return svg(ty + th + 4, b, "교육 SSAFY 15기 2026.01–12 · 학력 숭실대학교 컴퓨터학부 졸업 · 자격 정보처리기사 SQLD TOPCIT 수준 3 · 위치 서울 · 프론트엔드 영역 커밋 510/692 · 서체 준비 시간 913ms→149ms · 파트 간 문의 105건")

# ------------------------------------------------------------------ timeline
def marker(c, x, y, kind, now):
    fill = c["accent"] if now else c["surface"]
    stroke = c["accent"]
    if kind == "활동":
        stroke = c["muted"]
    if kind == "교육":
        return f'<rect x="{x-6}" y="{y-6}" width="12" height="12" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    if kind in ("자격", "수상"):
        f2 = c["ink"] if kind == "수상" else fill
        s2 = c["ink"] if kind == "수상" else stroke
        return f'<rect x="{x-5}" y="{y-5}" width="10" height="10" rx="2" fill="{f2}" stroke="{s2}" stroke-width="2" transform="rotate(45 {x} {y})"/>'
    return f'<circle cx="{x}" cy="{y}" r="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def tl(c):
    b, y = [], 8
    rx, tx = 8, 36
    starts = []
    for it in timeline:
        top = y
        starts.append(top + 8)
        # 날짜 + 종류 태그
        date = it["date"]
        b.append(text(tx, top + 13, date, 13, c["muted"], 400, MONO))
        dx = tx + width_of(date, 13) * 1.15 + 10
        kw = width_of(it["kind"], 12) + 20
        b.append(f'<rect x="{dx:.0f}" y="{top - 2}" width="{kw:.0f}" height="20" rx="10" fill="{c["tint"]}"/>')
        b.append(text(dx + 10, top + 12, it["kind"], 12, c["ink"], 500))
        y = top + 36
        b.append(text(tx, y, it["title"], 15, c["ink"], 600))
        y += 6
        if it.get("desc"):
            y += 20
            b.append(text(tx, y, it["desc"], 14, c["ink"]))
        for d in it.get("details", []):
            y += 20
            b.append(f'<circle cx="{tx + 3}" cy="{y - 4}" r="2" fill="{c["muted"]}"/>')
            b.append(text(tx + 12, y, d, 13, c["ink"]))
        y += 26
    total = y
    # 레일과 표식은 글 위에
    rail = [f'<rect x="{rx-1}" y="{starts[0]}" width="2" height="{starts[-1]-starts[0]}" rx="1" fill="{c["strong"]}"/>']
    for it, sy in zip(timeline, starts):
        rail.append(marker(c, rx, sy, it["kind"], it.get("now", False)))
    label = " · ".join(f'{i["date"]} {i["kind"]} {i["title"]}' for i in timeline)
    return svg(total, rail + b, "활동 타임라인: " + label)

# ------------------------------------------------------------------ skills
def sk(c):
    rows, y = [], 0
    ROW, NAME_W, LEVEL_W, PAD = 40, 170, 48, 8
    last = None
    for s in skills["rated"]:
        if s["group"] != last:
            y += 10 if last else 0
            rows.append(text(0, y + 22, s["group"], 12, c["muted"], 500, MONO, spacing="1.2"))
            y += 34; last = s["group"]
        cy = y + ROW / 2
        rows.append(text(0, cy + 5, s["name"], 15, c["ink"], 600))
        bar_w = W - NAME_W - LEVEL_W - PAD
        seg = (bar_w - 4 * 6) / 5
        for i in range(5):
            on = i < s["level"]
            fill = (c["accent"] if s["level"] >= 4 else c["strong"]) if on else c["line"]
            rows.append(f'<rect x="{NAME_W + i*(seg+6):.1f}" y="{cy-5}" width="{seg:.1f}" height="10" rx="3" fill="{fill}"/>')
        rows.append(text(W, cy + 5, f'{s["level"]}/5', 13, c["muted"], 400, MONO, "end"))
        y += ROW
    y += 14
    rows.append(text(0, y + 14, "써 본 것: " + " · ".join(skills["used"]), 13, c["muted"]))
    return svg(y + 34, rows, "스킬 별점")

for theme, c in T.items():
    for name, fn in (("hero", hero), ("about2", about), ("timeline", tl), ("skills", sk)):
        p = os.path.join(HERE, f"{name}-{theme}.svg")
        io.open(p, "w", encoding="utf-8", newline="\n").write(fn(c))
        print("wrote", os.path.basename(p))
