# -*- coding: utf-8 -*-
"""프로필 README 의 SVG 를 디자인 시스템 토큰으로 생성한다.
hero · skills 두 가지, 각각 라이트·다크.

- hero: 이름 · 첫 화면 문구 · 해결한 문제 숫자 세 개. 문구는 사이트 site.ts 의 person.title,
  숫자는 projects.ts 의 glocare-stage · glocare-resume · PinLog 서체 요청 시점과 같은 값을 여기 직접 적는다.
  사이트 값이 바뀌면 TITLE · HERO_STATS 를 같이 고친다(장표 2쪽과 같은 셋).
- 색은 portfolio/design-system/tokens.json(토큰 v2)을 읽는다.
- skills: portfolio/data/skills.json 의 rated(점 · can) · scale · used 를 읽는다.

about · timeline · how 그림은 README 에서 빠져 더 만들지 않는다(옛 SVG 파일은 남아 있음).
GitHub 는 웹폰트를 못 쓰므로 시스템 산세리프로 그린다. 글자 폭은 어림잡아 여유를 둔다."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "portfolio", "data")
skills = json.load(io.open(os.path.join(DATA, "skills.json"), encoding="utf-8"))

_tok = {t["name"]: t["value"] for t in json.load(io.open(os.path.join(HERE, "..", "..", "portfolio", "design-system", "tokens.json"), encoding="utf-8"))["color"]["tokens"]}
_MAP = dict(ground="ground", surface="surface", tint="tint", strong="tint-strong", ink="ink", soft="ink-soft", muted="muted", line="line", accent="accent", atext="accent-text", on="on-accent")
T = {theme: {k: _tok[v][theme] for k, v in _MAP.items()} for theme in ("light", "dark")}
W = 820
SANS = "Noto Sans KR, Apple SD Gothic Neo, Malgun Gothic, Segoe UI, sans-serif"
MONO = "Outfit, Apple SD Gothic Neo, Segoe UI, sans-serif"  # 숫자용. GitHub 에선 시스템 글꼴로 그려진다

# 첫 화면 문구. 사이트 site.ts person.title(세 줄)을 그림 폭에 맞춰 두 줄로 묶음. 둘째 줄만 강조색
# 2026.11.27 SSAFY 최종 장표의 캐치프레이즈로 바꿈(옛 문구 「시키시면 합니다. / AI 팀과 함께요.」)
TITLE = ("기준을 먼저 정하고, 바뀐 것은 숫자로 확인하는", "프론트엔드 개발자")

# 해결한 문제 셋. (프로젝트, 이전 값, 값, 분모, 단위, 설명)
HERO_STATS = [
    ("글로케어", "14", "0", "", "칸", "직원이 직접 켜던 진행 단계 칸. 결제 · 배정 기록이 쌓이면 스스로 바뀜"),
    ("글로케어", "4.41", "2.33", "", "초", "이력서 창이 그려지는 시간. 화면 밀림(CLS)도 0.55 → 0"),
    ("PinLog", "913", "149", "", "ms", "페이지 진입 후 검색 결과의 손글씨 서체를 요청하는 시점"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, weight=400, family=SANS, anchor="start", spacing=None):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{sp}>{esc(s)}</text>'


def width_of(s, size, mono=False):
    # 한글 1.0em, 공백 0.33em, 그 외 0.6em 어림. README의 SVG는 보는 사람 PC의 글꼴로 그려진다.
    # Windows 맑은 고딕은 한글 · 영문 모두 Noto Sans KR보다 넓어, 0.9 · 0.52로 어림하면 오른쪽 끝이 잘렸다(2026-11-26)
    if mono:
        return len(s) * size * 0.56
    return sum(size * (1.0 if ord(ch) > 0x2E80 else 0.33 if ch == " " else 0.6) for ch in s)


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
    b.append(text(PAD + 30, 23, "SSAFY 15기 · 포트폴리오", 13, c["atext"], 700))
    b.append(text(PAD, 64, "유승주", 30, c["ink"], 800))
    b.append(text(PAD + 96, 64, "(TrossYou)", 16, c["muted"], 400))
    b.append(text(PAD, 108, TITLE[0], 28, c["ink"], 800))
    tw0 = width_of(TITLE[1], 28) * 0.9
    b.append(f'<rect x="{PAD}" y="128" width="{tw0:.1f}" height="12" fill="{c["strong"]}"/>')
    b.append(text(PAD, 142, TITLE[1], 28, c["ink"], 800))

    GAP = 14
    tw = (W - PAD * 2 - GAP * 2) / 3
    ty = 168
    inner = tw - 40
    labels = [wrap(s[5], 12.5, inner) for s in HERO_STATS]
    th = 78 + 18 * max(len(l) for l in labels) + 10
    for i, (proj, frm, val, of, unit, _label) in enumerate(HERO_STATS):
        x = PAD + i * (tw + GAP)
        b.append(f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}"/>')
        b.append(text(x + 20, ty + 26, proj, 12, c["muted"], 700))
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
            b.append(text(x + 20, ty + 90 + 18 * k, line, 12.5, c["soft"]))
    stats = " · ".join(f'{s[5]} {(s[1] + " → ") if s[1] else ""}{s[2]}{s[3]}{s[4]}' for s in HERO_STATS)
    return svg(ty + th + 4, b, f"유승주 (TrossYou) · {' '.join(TITLE)} · {stats}")


# ------------------------------------------------------------------ skills
def dots(c, x, cy, level):
    r, gap = 4.5, 5
    strong = level >= 4
    out = []
    for k in range(5):
        on = k < level
        # 4점 이상은 초록, 3점 이하는 같은 초록을 옅게(흰 바탕에서 점이 사라지지 않게)
        op = "1" if strong else "0.45"
        fill = c["accent"] if on else "none"
        out.append(f'<circle cx="{x + r + k * (2 * r + gap):.1f}" cy="{cy:.1f}" r="{r - 0.75}" fill="{fill}" stroke="{c["accent"]}" stroke-width="1.5" fill-opacity="{op}" stroke-opacity="{op}"/>')
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
        rows.append(text(0, y + 14, g, 13, c["muted"], 700))
        y += 24
        for s in items:
            lines = wrap(s["can"], SIZE, CAN_W)
            h = 18 + LH * len(lines)
            first = y + 9 + 14
            rows.append(text(NAME_X, first, s["name"], 14, c["ink"], 600))
            rows += dots(c, DOT_X, first - 5, s["level"])
            for k, line in enumerate(lines):
                rows.append(text(CAN_X, first + LH * k, line, SIZE, c["soft"]))
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
