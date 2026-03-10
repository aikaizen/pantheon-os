from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

repo = Path(__file__).resolve().parents[2]
data = json.loads((repo / 'data' / 'pantheon-os.json').read_text())
out = Path(__file__).with_name('dashboard-mockup.png')

W, H = 1600, 2100
BG = (10, 13, 22)
PANEL = (18, 25, 42)
PANEL_2 = (24, 34, 56)
TEXT = (241, 245, 251)
MUTED = (152, 162, 179)
ACCENT = (124, 156, 255)
ACCENT_2 = (82, 215, 184)
WARN = (255, 211, 122)
DANGER = (255, 141, 141)
OK = (127, 240, 180)
BORDER = (34, 44, 66)

font_regular = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F12 = ImageFont.truetype(font_regular, 12)
F16 = ImageFont.truetype(font_regular, 16)
F18 = ImageFont.truetype(font_regular, 18)
F20 = ImageFont.truetype(font_bold, 20)
F24 = ImageFont.truetype(font_bold, 24)
F30 = ImageFont.truetype(font_bold, 30)
F56 = ImageFont.truetype(font_bold, 56)

def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ''
    for word in words:
        test = word if not cur else cur + ' ' + word
        if draw.textlength(test, font=font) <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def rr(draw, box, fill, outline=BORDER, radius=24, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def label(draw, x, y, text):
    draw.text((x, y), text.upper(), font=F12, fill=ACCENT_2)

def badge(draw, x, y, text, tone='info'):
    color = {'ok': OK, 'warn': WARN, 'danger': DANGER, 'info': ACCENT}.get(tone, ACCENT)
    tw = draw.textlength(text, font=F12)
    box = (x, y, x + tw + 24, y + 28)
    rr(draw, box, fill=(255, 255, 255, 10), outline=BORDER, radius=14)
    draw.text((x + 12, y + 7), text, font=F12, fill=color)
    return box[2]

def tone(value):
    v = str(value).lower()
    if v in {'approved','active','completed','strong','steady','scheduled','product'}:
        return 'ok'
    if v in {'pending','in_review','building','upcoming','mixed','pre-launch','service','experiment'}:
        return 'warn'
    if v in {'due','high','framing','mixed-signal','prototype'}:
        return 'danger'
    return 'info'

img = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)
for y in range(H):
    r = BG[0] + int(10 * (1 - y / H))
    g = BG[1] + int(12 * (1 - y / H))
    b = BG[2] + int(18 * (1 - y / H))
    draw.line((0, y, W, y), fill=(r, g, b))

margin = 48
sidebar_w = 260
main_x = margin + sidebar_w + 28
main_w = W - main_x - margin
rr(draw, (margin, 36, margin + sidebar_w, H - 36), fill=(8, 11, 18), outline=BORDER, radius=32)
rr(draw, (margin + 20, 56, margin + 74, 110), fill=ACCENT, outline=ACCENT, radius=16)
draw.text((margin + 39, 69), '◎', font=F24, fill=BG)
draw.text((margin + 90, 62), 'Pantheon OS', font=F24, fill=TEXT)
draw.text((margin + 90, 93), 'Prompt Engines control room', font=F16, fill=MUTED)
nav_items = ['Overview','Ventures','Goals','Heartbeats','Approvals','Budgets','Skills','Agents','Memory','Guidance']
y = 150
for item in nav_items:
    rr(draw, (margin + 18, y, margin + sidebar_w - 18, y + 38), fill=(12, 16, 28), outline=(12, 16, 28), radius=12)
    draw.text((margin + 34, y + 10), item, font=F16, fill=TEXT)
    y += 46
rr(draw, (margin + 18, H - 170, margin + sidebar_w - 18, H - 70), fill=(12, 16, 28), outline=BORDER, radius=18)
draw.text((margin + 34, H - 152), 'Compatibility', font=F16, fill=TEXT)
for i, line in enumerate(wrap(draw, 'data/company-os.json retained as an alias.', F12, sidebar_w - 80)):
    draw.text((margin + 34, H - 126 + i * 16), line, font=F12, fill=MUTED)

hero = (main_x, 36, main_x + main_w, 250)
rr(draw, hero, fill=PANEL, outline=BORDER, radius=32)
label(draw, main_x + 28, 60, 'Local-first company operating system')
draw.text((main_x + 28, 92), data['meta']['system_name'], font=F56, fill=TEXT)
for i, line in enumerate(wrap(draw, data['meta']['tagline'], F18, 720)):
    draw.text((main_x + 28, 160 + i * 24), line, font=F18, fill=MUTED)
end = badge(draw, main_x + 28, 214, 'Dashboard mockup', 'info')
badge(draw, end + 10, 214, 'Future host: dashboard.promptengines.com', 'ok')
chip_x = main_x + main_w - 280
for idx, (label_text, value) in enumerate([('Version', data['meta']['version']), ('Updated', data['meta']['updated_at'][:10]), ('Deployment target', 'dashboard.promptengines.com')]):
    cy = 58 + idx * 58
    rr(draw, (chip_x, cy, main_x + main_w - 28, cy + 48), fill=PANEL_2, outline=BORDER, radius=16)
    draw.text((chip_x + 14, cy + 8), label_text, font=F12, fill=MUTED)
    draw.text((chip_x + 14, cy + 24), value, font=F16, fill=TEXT)

summary = [('Ventures', str(data['summary']['venture_count'])), ('Open approvals', str(data['summary']['open_approvals'])), ('Due heartbeats', str(data['summary']['due_heartbeats'])), ('Active skills', str(data['summary']['active_skills'])), ('Monthly budget', f"${data['summary']['monthly_budget']:,}"), ('Forecast spend', f"${data['summary']['monthly_forecast']:,}")]
card_w = (main_w - 5 * 16) // 6
x = main_x
y = 276
for label_text, value in summary:
    rr(draw, (x, y, x + card_w, y + 108), fill=PANEL, outline=BORDER, radius=22)
    draw.text((x + 16, y + 16), label_text, font=F16, fill=MUTED)
    draw.text((x + 16, y + 48), value, font=F30, fill=TEXT)
    x += card_w + 16

def section_title(x, y, title, subtitle):
    draw.text((x, y), title, font=F30, fill=TEXT)
    draw.text((x, y + 38), subtitle, font=F16, fill=MUTED)

vy = 430
section_title(main_x, vy, 'Portfolio', 'Canonical ventures, stages, health, and next actions.')
card_gap = 18
cols = 3
vw = (main_w - card_gap * (cols - 1)) // cols
vh = 170
start_y = vy + 76
for i, venture in enumerate(data['ventures'][:6]):
    row, col = divmod(i, cols)
    x = main_x + col * (vw + card_gap)
    y = start_y + row * (vh + card_gap)
    rr(draw, (x, y, x + vw, y + vh), fill=PANEL, outline=BORDER, radius=24)
    draw.text((x + 18, y + 16), venture['name'], font=F20, fill=TEXT)
    bx = x + 18
    bx = badge(draw, bx, y + 48, venture['stage'], tone(venture['stage'])) + 8
    bx = badge(draw, bx, y + 48, venture['status'], tone(venture['status'])) + 8
    badge(draw, bx, y + 48, venture['health'], tone(venture['health']))
    draw.text((x + 18, y + 86), f"Owner: {venture['owner']}", font=F16, fill=TEXT)
    for j, line in enumerate(wrap(draw, venture['next_action'], F12, vw - 36)):
        if j > 2:
            break
        draw.text((x + 18, y + 112 + j * 16), line, font=F12, fill=MUTED)

gy = start_y + 2 * (vh + card_gap) + 22
section_title(main_x, gy, 'Goal tree', 'Company → venture → project hierarchy with task decomposition.')
rr(draw, (main_x, gy + 76, main_x + main_w, gy + 420), fill=PANEL, outline=BORDER, radius=28)
root_goal = data['goals'][0]
draw.text((main_x + 24, gy + 96), root_goal['title'], font=F24, fill=TEXT)
badge(draw, main_x + 24, gy + 132, root_goal['status'], tone(root_goal['status']))
draw.text((main_x + 24, gy + 170), f"Target: {root_goal['target_metric']}", font=F16, fill=MUTED)
subs = [g for g in data['goals'][1:4]]
base_y = gy + 220
for idx, goal in enumerate(subs):
    y0 = base_y + idx * 58
    draw.line((main_x + 36, y0 + 10, main_x + 60, y0 + 10), fill=ACCENT, width=2)
    draw.text((main_x + 72, y0), goal['title'], font=F18, fill=TEXT)
    draw.text((main_x + 72, y0 + 24), f"{goal['owner']} · due {goal['target_date']}", font=F12, fill=MUTED)

hy = gy + 470
col_w = (main_w - 18) // 2
section_title(main_x, hy, 'Heartbeats', 'Recurring loops, sitreps, and wake cycles.')
section_title(main_x + col_w + 18, hy, 'Approvals', 'Explicit governance gates for higher-risk actions.')
rr(draw, (main_x, hy + 76, main_x + col_w, hy + 420), fill=PANEL, outline=BORDER, radius=28)
rr(draw, (main_x + col_w + 18, hy + 76, main_x + main_w, hy + 420), fill=PANEL, outline=BORDER, radius=28)
for idx, hb in enumerate(data['heartbeats'][:4]):
    y0 = hy + 96 + idx * 78
    draw.text((main_x + 20, y0), hb['name'], font=F18, fill=TEXT)
    badge(draw, main_x + 20, y0 + 28, hb['status'], tone(hb['status']))
    draw.text((main_x + 20, y0 + 54), f"{hb['cadence']} · {hb['owner']} · {hb['budget_minutes']} min", font=F12, fill=MUTED)
for idx, ap in enumerate(data['approvals'][:4]):
    y0 = hy + 96 + idx * 78
    x0 = main_x + col_w + 38
    title = ap['title']
    if len(title) > 44:
        title = title[:44] + '…'
    draw.text((x0, y0), title, font=F18, fill=TEXT)
    bx = badge(draw, x0, y0 + 28, ap['status'], tone(ap['status'])) + 8
    badge(draw, bx, y0 + 28, 'risk: ' + ap['risk'], tone(ap['risk']))
    draw.text((x0, y0 + 54), f"Approver: {ap['approver']} · Due {ap['due_date']}", font=F12, fill=MUTED)

by = hy + 470
section_title(main_x, by, 'Budget visibility', 'Company, venture, and agent runtime cost posture.')
section_title(main_x + col_w + 18, by, 'Skill library', 'First-class operational assets with governance and tests.')
rr(draw, (main_x, by + 76, main_x + col_w, by + 360), fill=PANEL, outline=BORDER, radius=28)
rr(draw, (main_x + col_w + 18, by + 76, main_x + main_w, by + 360), fill=PANEL, outline=BORDER, radius=28)
company = data['budgets']['company']
draw.text((main_x + 20, by + 96), f"Company runtime posture: ${company['spent']:,} / ${company['allocated']:,}", font=F20, fill=TEXT)
draw.text((main_x + 20, by + 126), f"Forecast ${company['forecast']:,}", font=F16, fill=MUTED)
for idx, row in enumerate(data['budgets']['by_agent']):
    y0 = by + 166 + idx * 34
    draw.text((main_x + 20, y0), row['name'], font=F16, fill=TEXT)
    draw.text((main_x + 210, y0), f"${row['spent']:,} / ${row['allocated']:,}", font=F16, fill=MUTED)
    draw.rounded_rectangle((main_x + 360, y0 + 6, main_x + col_w - 24, y0 + 20), radius=7, fill=(35, 44, 66))
    pct = min(1.0, row['spent'] / row['allocated'])
    draw.rounded_rectangle((main_x + 360, y0 + 6, main_x + 360 + int((col_w - 384) * pct), y0 + 20), radius=7, fill=ACCENT)
for idx, skill in enumerate(data['skills']):
    y0 = by + 96 + idx * 48
    x0 = main_x + col_w + 38
    draw.text((x0, y0), skill['name'], font=F18, fill=TEXT)
    draw.text((x0, y0 + 22), f"{skill['owner']} · {skill['review_cadence']} · {skill['status']}", font=F12, fill=MUTED)

footer_y = H - 54
draw.text((main_x, footer_y), 'Pantheon OS dashboard mockup for Prompt Engines — future destination: dashboard.promptengines.com', font=F16, fill=MUTED)
img.save(out)
print(out)
