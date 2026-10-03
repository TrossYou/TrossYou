# -*- coding: utf-8 -*-
"""프로필 README 의 SVG 를 디자인 시스템 토큰으로 생성한다.
hero · about · timeline · skills, 각각 라이트·다크. 데이터는 portfolio/data/ 에서 읽는다.
GitHub 는 웹폰트를 못 쓰므로 시스템 산세리프로 그린다. 글자 폭은 어림잡아 여유를 둔다."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "portfolio", "data")
skills = json.load(io.open(os.path.join(DATA, "skills.json"), encoding="utf-8"))
timeline = json.load(io.open(os.path.join(DATA, "timeline.json"), encoding="utf-8"))
import re
_site = io.open(os.path.join(DATA, "site.ts"), encoding="utf-8").read()
traits = [dict(trait=m[0], evidence=m[1], label=m[2]) for m in re.findall(
    r"trait: '([^']+)',\s*evidence: '([^']+)',\s*sourceLabel: '([^']+)'", _site)]

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
    """이름과 통계 타일을 한 단계 작게. 좌우에 PAD 만큼 여백을 둬 README 본문 가장자리에 붙지 않게 한다"""
    PAD = 24
    b = []
    b.append(f'<rect x="{PAD}" y="18" width="20" height="2" fill="{c["accent"]}"/>')
    b.append(text(PAD + 30, 23, "FRONTEND DEVELOPER", 11, c["muted"], 500, MONO, spacing="1.4"))
    b.append(text(PAD, 66, "유승주", 34, c["ink"], 700))
    b.append(text(PAD + 112, 66, "(TrossYou)", 17, c["muted"], 400))
    y = 102
    b.append(f'<text x="{PAD}" y="{y}" font-family="{SANS}" font-size="16" fill="{c["ink"]}">무엇을 결정했고, 무엇이 <tspan fill="{c["atext"]}" font-weight="600">틀렸고</tspan>, 무엇을 남겼는지</text>')
    b.append(text(PAD, y + 25, "적어 두는 프론트엔드 개발자입니다.", 16, c["ink"]))
    # 오른쪽 통계 타일 (surface + line, radius 14)
    tw, th = 224, 116
    tx, ty = W - PAD - tw, 12
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}"/>')
    b.append(text(tx + 20, ty + 28, "검색 결과 서체 준비 시간", 12, c["ink"], 500))
    b.append(text(tx + 20, ty + 45, "PinLog · Chrome 성능 패널", 11, c["muted"]))
    b.append(text(tx + 20, ty + 82, "913ms", 14, c["muted"], 400, MONO))
    b.append(text(tx + 72, ty + 82, "→", 14, c["muted"], 400, MONO))
    b.append(text(tx + 92, ty + 84, "149", 28, c["atext"], 600, MONO))
    b.append(text(tx + 150, ty + 82, "ms", 14, c["muted"], 400, MONO))
    b.append(f'<rect x="{tx + 20}" y="{ty + 96}" width="{tw - 40}" height="3" rx="1.5" fill="{c["line"]}"/>')
    b.append(f'<rect x="{tx + 20}" y="{ty + 96}" width="{int((tw - 40) * 149 / 913)}" height="3" rx="1.5" fill="{c["accent"]}"/>')
    return svg(144, b, "유승주 (TrossYou) · 프론트엔드 개발자 · 무엇을 결정했고, 무엇이 틀렸고, 무엇을 남겼는지 적어 두는 프론트엔드 개발자입니다 · 검색 결과 서체 준비 시간 913ms → 149ms")

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
    """프로젝트는 빈 원(진행 중이면 남색 채움). 교육은 페리윙클 정사각형, 자격은 페리윙클 마름모, 수상은 잉크 마름모.
    빈 도형끼리는 12px 에서 구분되지 않아 교육·자격은 채움으로도 가른다"""
    if kind == "교육":
        return f'<rect x="{x-6}" y="{y-6}" width="12" height="12" fill="{c["strong"]}"/>'
    if kind == "자격":
        return f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="{c["strong"]}" transform="rotate(45 {x} {y})"/>'
    if kind == "수상":
        return f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="{c["ink"]}" transform="rotate(45 {x} {y})"/>'
    stroke = c["muted"] if kind == "활동" else c["accent"]
    fill = c["accent"] if now else c["surface"]
    return f'<circle cx="{x}" cy="{y}" r="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def wrap(s, size, max_w):
    """어림 폭으로 줄을 나눈다. 공백에서만 끊는다"""
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and width_of(cand, size) > max_w:
            lines.append(cur); cur = w
        else:
            cur = cand
    if cur: lines.append(cur)
    return lines

def tl_column(c, items, x0, col_w, col_id, fade_in):
    """한 열. 레일 하나에 항목들. (요소들, 높이) 반환"""
    b, y = [], 8
    rx, tx = x0 + 8, x0 + 36
    text_w = col_w - 36
    starts = []
    for it in items:
        top = y
        starts.append(top + 8)
        date = it["date"]
        b.append(text(tx, top + 13, date, 13, c["muted"], 400, MONO))
        dx = tx + width_of(date, 13) * 1.15 + 10
        tl_w = 12 * 0.92 * len(it["kind"])
        kw = tl_w + 20
        chip = c["strong"] if it["kind"] in ("교육", "자격") else c["tint"]
        b.append(f'<rect x="{dx:.0f}" y="{top - 2}" width="{kw:.0f}" height="20" rx="10" fill="{chip}"/>')
        b.append(f'<text x="{dx + 10:.1f}" y="{top + 12}" font-family="{SANS}" font-size="12" font-weight="500" fill="{c["ink"]}" textLength="{tl_w:.1f}" lengthAdjust="spacingAndGlyphs">{esc(it["kind"])}</text>')
        y = top + 36
        b.append(text(tx, y, it["title"], 15, c["ink"], 600))
        y += 6
        for line in wrap(it.get("desc", ""), 14, text_w) if it.get("desc") else []:
            y += 20
            b.append(text(tx, y, line, 14, c["ink"]))
        y += 26
    # 레일은 마지막 표식 아래로 더 내려가며 배경으로 스며든다. 둘째 열은 위에서 스며들어 온다
    top = -8 if fade_in else starts[0]
    bottom = y + 8
    grad = f"url(#rail-{col_id})"
    rail = [f'<rect x="{rx-1}" y="{top}" width="2" height="{bottom - top}" rx="1" fill="{grad}"/>']
    for it, sy in zip(items, starts):
        rail.append(marker(c, rx, sy, it["kind"], it.get("now", False)))
    return rail + b, y

def tl(c):
    """두 열. 왼쪽이 과거, 오른쪽이 최근. 자격은 축에 섞지 않고 맨 아래 한 줄에 칩으로 둔다.
    자격은 기간이 없고 설명도 없어 축 위에서는 빈 칸만 늘린다"""
    GAP = 48
    col_w = (W - GAP) / 2
    main = [i for i in timeline if i["kind"] != "자격"]
    certs = [i for i in timeline if i["kind"] == "자격"]
    half = (len(main) + 1) // 2
    left, hl = tl_column(c, main[:half], 0, col_w, "l", fade_in=False)
    right, hr = tl_column(c, main[half:], col_w + GAP, col_w, "r", fade_in=True)
    y = max(hl, hr) + 8
    b = []
    b.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{c["line"]}"/>')
    y += 30
    b.append(text(0, y, "자격", 12, c["muted"], 500, MONO, spacing="1.2"))
    x = 60
    for it in certs:
        date, name = it["date"], it["title"]
        dw = width_of(date, 12) * 1.15
        nw = width_of(name, 13)
        cw = 12 + dw + 8 + nw + 12
        b.append(f'<rect x="{x:.0f}" y="{y - 14}" width="{cw:.0f}" height="22" rx="11" fill="{c["tint"]}"/>')
        b.append(text(x + 12, y + 1, date, 12, c["muted"], 400, MONO))
        b.append(text(x + 12 + dw + 8, y + 1, name, 13, c["ink"], 500))
        x += cw + 10
    defs = f'''<defs>
<linearGradient id="rail-l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["strong"]}"/><stop offset="0.82" stop-color="{c["strong"]}"/><stop offset="1" stop-color="{c["strong"]}" stop-opacity="0"/></linearGradient>
<linearGradient id="rail-r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["strong"]}" stop-opacity="0"/><stop offset="0.14" stop-color="{c["strong"]}"/><stop offset="0.82" stop-color="{c["strong"]}"/><stop offset="1" stop-color="{c["strong"]}" stop-opacity="0"/></linearGradient>
</defs>'''
    label = " · ".join(f'{i["date"]} {i["kind"]} {i["title"]}' for i in timeline)
    return svg(y + 16, [defs] + left + right + b, "활동 타임라인: " + label)

# ------------------------------------------------------------------ skills
def sk(c):
    """묶음 머리는 한 줄 전체, 항목은 두 열로 흐른다. 이름은 열 왼쪽 끝, 점은 열 오른쪽 끝(space-between).
    줄 밑선은 전체 폭 하나. 기준은 맨 아래 오른쪽 정렬"""
    groups = []
    for s in skills["rated"]:
        if not groups or groups[-1][0] != s["group"]:
            groups.append((s["group"], []))
        groups[-1][1].append(s)
    COLS, GAP, ROW = 2, 48, 36
    col_w = (W - GAP * (COLS - 1)) / COLS
    rows, y = [], 0
    for gi, (g, items) in enumerate(groups):
        y += 0 if gi == 0 else 24
        rows.append(text(0, y + 14, g, 12, c["muted"], 500, MONO, spacing="1.2"))
        y += 24
        for i, s in enumerate(items):
            col = i % COLS
            if col == 0 and i > 0:
                y += ROW
            x0 = col * (col_w + GAP)
            cy = y + ROW / 2
            rows.append(text(x0, cy + 5, s["name"], 15, c["ink"], 600))
            r, gap = 4.5, 5
            dx0 = x0 + col_w - (5 * 2 * r + 4 * gap) + r
            for k in range(5):
                on = k < s["level"]
                strong = s["level"] >= 4
                fill = (c["accent"] if strong else c["strong"]) if on else "none"
                stroke = c["accent"] if strong else c["strong"]
                rows.append(f'<circle cx="{dx0 + k*(2*r+gap):.1f}" cy="{cy:.1f}" r="{r - 0.75}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            if col == 0:
                n_in_row = min(COLS, len(items) - i)
                line_w = n_in_row * col_w + (n_in_row - 1) * GAP
                rows.append(f'<rect x="0" y="{y + ROW - 1}" width="{line_w:.0f}" height="1" fill="{c["line"]}"/>')
        y += ROW
    y += 20
    rows.append(text(0, y + 12, "써 본 것: " + " · ".join(skills["used"]), 12, c["muted"]))
    y += 12
    for line in skills["scale"].split(" · "):
        y += 18
        rows.append(text(W, y + 12, line, 12, c["muted"], anchor="end"))
    return svg(y + 24, rows, "스킬 별점. " + skills["scale"])

# ------------------------------------------------------------------ how i work
def how(c):
    """성향 카드 셋. 라벨, 한 일 한 문장, 출처. 링크는 SVG 안에 못 두므로 README 에서 그림 아래 글자로 건다"""
    GAP = 16
    n = len(traits)
    cw = (W - GAP * (n - 1)) / n
    pad, size = 20, 13
    cols = []
    maxh = 0
    for i, t in enumerate(traits):
        x = i * (cw + GAP)
        body = []
        y = 34
        body.append(text(x + pad, y, t["trait"], 15, c["ink"], 600))
        y += 14
        for line in wrap(t["evidence"], size, cw - pad * 2):
            y += 21
            body.append(text(x + pad, y, line, size, c["ink"]))
        y += 14
        src = []
        for line in wrap("근거 · " + t["label"], 11, cw - pad * 2):
            y += 16
            src.append(text(x + pad, y, line, 11, c["muted"]))
        body += src
        cols.append((x, body))
        maxh = max(maxh, y + 20)
    out = []
    for x, body in cols:
        out.append(f'<rect x="{x:.0f}" y="1" width="{cw:.0f}" height="{maxh - 2}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}"/>')
        out += body
    return svg(maxh, out, "How I Work: " + " · ".join(f'{t["trait"]}. {t["evidence"]}' for t in traits))

for theme, c in T.items():
    for name, fn in (("hero", hero), ("about2", about), ("timeline", tl), ("skills", sk), ("how", how)):
        p = os.path.join(HERE, f"{name}-{theme}.svg")
        io.open(p, "w", encoding="utf-8", newline="\n").write(fn(c))
        print("wrote", os.path.basename(p))
