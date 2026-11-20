# -*- coding: utf-8 -*-
"""프로필 README 의 SVG 를 디자인 시스템 토큰으로 생성한다.
hero · skills 두 가지, 각각 라이트·다크.

- hero: 이름 · 한 줄 소개 · 숫자 셋. 숫자 셋은 사이트 site.ts 의 heroStats
  (glocare-stage · glocare-dashboard · finch-commits)와 같은 값을 여기 직접 적는다.
  문구 규칙이 바뀌는 중이라 site.ts 를 읽지 않는다. 사이트 값이 바뀌면 HERO_STATS 를 같이 고친다.
- skills: portfolio/data/skills.json 의 rated(점 · can) · scale · used 를 읽는다.

about · timeline · how 그림은 README 에서 빠져 더 만들지 않는다(옛 SVG 파일은 남아 있음).
GitHub 는 웹폰트를 못 쓰므로 시스템 산세리프로 그린다. 글자 폭은 어림잡아 여유를 둔다."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "portfolio", "data")
skills = json.load(io.open(os.path.join(DATA, "skills.json"), encoding="utf-8"))

T = {
    "light": dict(ground="#fafafa", surface="#ffffff", tint="#e7ecfa", strong="#b9c7f2", ink="#1c1f27", muted="#5d6270", line="#e2e4ea", accent="#2e4a8b", atext="#2e4a8b", on="#ffffff"),
    "dark": dict(ground="#0f1114", surface="#17191f", tint="#1f2744", strong="#3b4c86", ink="#e9eaee", muted="#a1a5b0", line="#2a2d36", accent="#4c6cb3", atext="#9db1ec", on="#ffffff"),
}
W = 820
SANS = "IBM Plex Sans KR, Apple SD Gothic Neo, Malgun Gothic, Segoe UI, sans-serif"
MONO = "JetBrains Mono, Cascadia Mono, Consolas, monospace"

# 한 줄 소개. 모든 산출물이 같은 문구를 쓴다. 가운데 조각만 강조색
INTRO = ("AI 코딩 에이전트를 역할별로 나눠 운영하며,", "수동 업무를 데이터로 연결하는", " 프론트엔드 개발자")

# 사이트 heroStats 와 같은 값. (프로젝트, 이전 값, 값, 분모, 단위, 설명)
HERO_STATS = [
    ("GLOCARE", "14", "0", "", "칸", "직원이 수동으로 켜던 진행 단계 칸. 결제 · 배정 기록으로 자동 판정"),
    ("GLOCARE", "1,300", "659", "", "ms", "배포 사이트 대시보드 첫 화면 문서 응답"),
    ("FINCH", "", "510", "/ 692", "", "프론트엔드 영역 커밋 (74%)"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, weight=400, family=SANS, anchor="start", spacing=None):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{sp}>{esc(s)}</text>'


def width_of(s, size, mono=False):
    # 한글 0.9em, 공백 0.3em, 그 외 0.52em 어림(시스템 산세리프 실측보다 조금 넉넉하게). 고정폭 글꼴은 0.62em
    if mono:
        return len(s) * size * 0.62
    return sum(size * (0.9 if ord(ch) > 0x2E80 else 0.3 if ch == " " else 0.52) for ch in s)


def wrap(s, size, max_w):
    """어림 폭으로 줄을 나눈다. 공백에서만 끊는다"""
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and width_of(cand, size) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def svg(h, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h:.0f}" width="{W}" height="{h:.0f}" role="img" aria-label="{esc(label)}">\n' + "\n".join(body) + "\n</svg>\n"


# ------------------------------------------------------------------ hero
def hero(c):
    """위에 이름과 한 줄 소개, 아래에 숫자 타일 셋. 좌우에 PAD 만큼 여백을 둬 README 본문 가장자리에 붙지 않게 한다"""
    PAD = 24
    b = []
    b.append(f'<rect x="{PAD}" y="18" width="20" height="2" fill="{c["accent"]}"/>')
    b.append(text(PAD + 30, 23, "FRONTEND DEVELOPER · SSAFY 15기", 11, c["muted"], 500, MONO, spacing="1.4"))
    b.append(text(PAD, 68, "유승주", 34, c["ink"], 700))
    b.append(text(PAD + 104, 68, "(TrossYou)", 17, c["muted"], 400))
    b.append(text(PAD, 110, INTRO[0], 20, c["ink"], 500))
    b.append(f'<text x="{PAD}" y="140" font-family="{SANS}" font-size="20" font-weight="500" fill="{c["ink"]}">'
             f'<tspan fill="{c["atext"]}" font-weight="700">{esc(INTRO[1])}</tspan>{esc(INTRO[2])}</text>')

    GAP = 14
    tw = (W - PAD * 2 - GAP * 2) / 3
    ty = 168
    inner = tw - 40
    labels = [wrap(s[5], 12.5, inner) for s in HERO_STATS]
    th = 78 + 18 * max(len(l) for l in labels) + 10
    for i, (proj, frm, val, of, unit, _label) in enumerate(HERO_STATS):
        x = PAD + i * (tw + GAP)
        b.append(f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}"/>')
        b.append(text(x + 20, ty + 26, proj, 10.5, c["muted"], 500, MONO, spacing="1.2"))
        vx = x + 20
        vy = ty + 62
        if frm:
            b.append(text(vx, vy, frm, 15, c["muted"], 400, MONO))
            vx += width_of(frm, 15, True) + 6
            b.append(text(vx, vy, "→", 15, c["muted"], 400, MONO))
            vx += width_of("→", 15, True) + 8
        b.append(text(vx, vy, val, 30, c["atext"], 600, MONO))
        vx += width_of(val, 30, True) + 6
        if of:
            b.append(text(vx, vy, of, 15, c["muted"], 400, MONO))
        if unit:
            b.append(text(vx, vy, unit, 15, c["muted"], 400, MONO if unit.isascii() else SANS))
        for k, line in enumerate(labels[i]):
            b.append(text(x + 20, ty + 90 + 18 * k, line, 12.5, c["ink"]))
    stats = " · ".join(f'{s[5]} {(s[1] + " → ") if s[1] else ""}{s[2]}{s[3]}{s[4]}' for s in HERO_STATS)
    return svg(ty + th + 4, b, f"유승주 (TrossYou) · {''.join(INTRO)} · {stats}")


# ------------------------------------------------------------------ skills
def dots(c, x, cy, level):
    r, gap = 4.5, 5
    strong = level >= 4
    out = []
    for k in range(5):
        on = k < level
        fill = (c["accent"] if strong else c["strong"]) if on else "none"
        stroke = c["accent"] if strong else c["strong"]
        out.append(f'<circle cx="{x + r + k * (2 * r + gap):.1f}" cy="{cy:.1f}" r="{r - 0.75}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    return out


def sk(c):
    """한 줄에 이름 · 점 · 할 수 있는 것. 묶음 머리는 한 줄 전체. 아래에 점 기준과 써 본 것"""
    groups = []
    for s in skills["rated"]:
        if not groups or groups[-1][0] != s["group"]:
            groups.append((s["group"], []))
        groups[-1][1].append(s)
    NAME_X, DOT_X, CAN_X = 0, 128, 206
    CAN_W = W - CAN_X
    SIZE, LH = 12.5, 19
    rows, y = [], 0
    for gi, (g, items) in enumerate(groups):
        y += 0 if gi == 0 else 26
        rows.append(text(0, y + 14, g, 12, c["muted"], 500, MONO, spacing="1.2"))
        y += 24
        for s in items:
            lines = wrap(s["can"], SIZE, CAN_W)
            h = 18 + LH * len(lines)
            first = y + 9 + 14
            rows.append(text(NAME_X, first, s["name"], 14, c["ink"], 600))
            rows += dots(c, DOT_X, first - 5, s["level"])
            for k, line in enumerate(lines):
                rows.append(text(CAN_X, first + LH * k, line, SIZE, c["ink"]))
            y += h
            rows.append(f'<rect x="0" y="{y - 1:.0f}" width="{W}" height="1" fill="{c["line"]}"/>')
    y += 28
    # 범례: 4점 · 3점 견본 + 기준 문장
    rows += dots(c, 0, y - 4, 4)
    rows.append(text(72, y, "4점", 12, c["muted"]))
    rows += dots(c, 110, y - 4, 3)
    rows.append(text(182, y, "3점", 12, c["muted"]))
    for line in wrap(skills["scale"], 12, W):
        y += 20
        rows.append(text(0, y, line, 12, c["muted"]))
    y += 8
    for line in wrap("써 본 것: " + " · ".join(skills["used"]), 12, W):
        y += 20
        rows.append(text(0, y, line, 12, c["muted"]))
    label = "할 수 있는 것. " + " · ".join(f'{s["name"]} {s["level"]}점: {s["can"]}' for s in skills["rated"]) + " " + skills["scale"] + " 써 본 것: " + ", ".join(skills["used"])
    return svg(y + 12, rows, label)


for theme, c in T.items():
    for name, fn in (("hero", hero), ("skills", sk)):
        p = os.path.join(HERE, f"{name}-{theme}.svg")
        io.open(p, "w", encoding="utf-8", newline="\n").write(fn(c))
        print("wrote", os.path.basename(p))
