import html
import json
import math
import random
import urllib.request
from datetime import datetime

random.seed(2027)

# ---------------------------------------------------------
# 1. Generate Avengers: Doomsday Metallic Headers (Zero Emojis)
# ---------------------------------------------------------
def create_doomsday_header(filename, kicker, title):
    kicker_xml = html.escape(kicker)
    title_xml = html.escape(title)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 76" width="100%" height="100%">
  <defs>
    <linearGradient id="steelBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#040706" stop-opacity="0"/>
      <stop offset="14%" stop-color="#0b1310" stop-opacity="0.96"/>
      <stop offset="50%" stop-color="#121e19" stop-opacity="0.98"/>
      <stop offset="86%" stop-color="#0b1310" stop-opacity="0.96"/>
      <stop offset="100%" stop-color="#040706" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="emeraldBeam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0"/>
      <stop offset="18%" stop-color="#059669"/>
      <stop offset="50%" stop-color="#4ade80"/>
      <stop offset="82%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="chromeTitle" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="48%" stop-color="#cbd5e1"/>
      <stop offset="52%" stop-color="#86efac"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
    <filter id="emeraldGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Beveled armored titanium plate -->
  <polygon points="56,8 864,8 890,26 890,50 864,68 56,68 30,50 30,26" fill="url(#steelBg)" stroke="#1f332a" stroke-width="1.4"/>

  <!-- Top and bottom arcane emerald conduits -->
  <rect x="60" y="7" width="800" height="2" fill="url(#emeraldBeam)" filter="url(#emeraldGlow)"/>
  <rect x="120" y="67" width="680" height="1.5" fill="url(#emeraldBeam)" opacity="0.75"/>

  <!-- Left & right titanium rivets / energy nodes -->
  <polygon points="52,38 62,31 72,38 62,45" fill="#10b981" filter="url(#emeraldGlow)"/>
  <polygon points="868,38 858,31 848,38 858,45" fill="#10b981" filter="url(#emeraldGlow)"/>
  <circle cx="92" cy="38" r="2.2" fill="#4ade80" opacity="0.7"/>
  <circle cx="828" cy="38" r="2.2" fill="#4ade80" opacity="0.7"/>

  <!-- Kicker -->
  <text x="460" y="27" text-anchor="middle" font-family="'Segoe UI', 'Arial', sans-serif" font-size="10.5" font-weight="700" letter-spacing="4.8" fill="#4ade80">{kicker_xml}</text>

  <!-- Metallic Cinema Title -->
  <text x="460" y="55" text-anchor="middle" font-family="'Impact', 'Arial Black', 'Franklin Gothic Heavy', sans-serif" font-size="25" letter-spacing="3.5" fill="url(#chromeTitle)" filter="url(#emeraldGlow)">{title_xml}</text>
</svg>
'''
    with open(f"public/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)

create_doomsday_header("doomsday-header-specialties.svg", "LATVERIA CITADEL // CORE DIRECTIVES", "SPECIALTIES & ARCHITECTURE")
create_doomsday_header("doomsday-header-stack.svg", "TITANIUM ARSENAL // SYSTEMS & PROTOCOLS", "TECH STACK & ARMORY")
create_doomsday_header("doomsday-header-stats.svg", "MULTIVERSE TELEMETRY // DIAGNOSTICS", "DOOMSDAY RECORD & STATS")
create_doomsday_header("doomsday-header-activity.svg", "ARCANE PLASMA MATRIX // LIVE TELEMETRY", "DOOMSDAY ACTIVITY BOARD")

# ---------------------------------------------------------
# 2. Generate Realistic Avengers: Doomsday Activity Matrix SVG
# ---------------------------------------------------------
url = "https://github-contributions-api.jogruber.de/v4/jeremialex04?y=last"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))

contributions = data.get("contributions", [])
total_last_year = data.get("total", {}).get("lastYear", sum(c.get("count", 0) for c in contributions))

weeks = []
current_week = [None] * 7
for item in contributions:
    dt = datetime.strptime(item["date"], "%Y-%m-%d")
    dow = (dt.weekday() + 1) % 7
    if dow == 0 and any(x is not None for x in current_week):
        weeks.append(current_week)
        current_week = [None] * 7
    current_week[dow] = item

if any(x is not None for x in current_week):
    weeks.append(current_week)

num_weeks = len(weeks)

width = 940
height = 345
grid_x0 = 62
grid_y0 = 110
cell_size = 12.2
cell_gap = 3.6
step = cell_size + cell_gap

forge_duration = 10.0
hold_duration = 5.5
total_cycle = forge_duration + hold_duration

# Avengers: Doomsday Titanium & Emerald Plasma Palette
level_colors = {
    0: "#0c1411",  # Dormant titanium slot
    1: "#065f46",  # Dark Latverian emerald
    2: "#059669",  # Arcane emerald energy
    3: "#10b981",  # Bright Doomsday green
    4: "#4ade80",  # Overcharged incursion plasma
}

months_es = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
month_labels = []
last_month = None
for w_idx, week in enumerate(weeks):
    for day in week:
        if day is not None:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            if dt.day <= 7 and dt.month != last_month:
                x_pos = grid_x0 + w_idx * step
                if not month_labels or (x_pos - month_labels[-1][1]) >= 30:
                    month_labels.append((months_es[dt.month - 1], x_pos))
                    last_month = dt.month
            break

# Vector Hexagonal Rivet Helper
def hex_points(cx, cy, r=5.5):
    pts = []
    for i in range(6):
        a = math.radians(30 + i * 60)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)

svg_parts = []
svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <!-- Brushed Dark Titanium Armored Plate -->
    <linearGradient id="armorPlate" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050807"/>
      <stop offset="45%" stop-color="#0c1511"/>
      <stop offset="75%" stop-color="#08100d"/>
      <stop offset="100%" stop-color="#040706"/>
    </linearGradient>

    <!-- Ambient Emerald Incursion Glows -->
    <radialGradient id="incursionLeft" cx="10%" cy="15%" r="48%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="#065f46" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#040706" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="incursionRight" cx="90%" cy="85%" r="48%">
      <stop offset="0%" stop-color="#4ade80" stop-opacity="0.16"/>
      <stop offset="60%" stop-color="#059669" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#040706" stop-opacity="0"/>
    </radialGradient>

    <!-- Metallic Bevel Chrome Gradient -->
    <linearGradient id="chromeMetal" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#e2e8f0"/>
      <stop offset="45%" stop-color="#94a3b8"/>
      <stop offset="55%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>

    <!-- Arcane Emerald Energy Bar -->
    <linearGradient id="energyBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#064e3b"/>
      <stop offset="35%" stop-color="#059669"/>
      <stop offset="70%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#86efac"/>
    </linearGradient>

    <!-- Vertical Plasma Scanner Beam -->
    <linearGradient id="plasmaBeamH" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0"/>
      <stop offset="32%" stop-color="#10b981" stop-opacity="0.55"/>
      <stop offset="50%" stop-color="#dcfce7" stop-opacity="1"/>
      <stop offset="68%" stop-color="#10b981" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </linearGradient>

    <!-- Radial Energy Impact Aura -->
    <radialGradient id="plasmaImpact" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ecfdf5" stop-opacity="0.95"/>
      <stop offset="32%" stop-color="#4ade80" stop-opacity="0.65"/>
      <stop offset="68%" stop-color="#059669" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <!-- Brushed Steel Micro-Texture -->
    <filter id="steelGrain" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04 0.65" numOctaves="2" seed="19" result="noise"/>
      <feColorMatrix type="matrix" values="
        0 0 0 0 0.60
        0 0 0 0 0.85
        0 0 0 0 0.72
        0 0 0 0.045 0" in="noise" result="tinted"/>
      <feComposite in="tinted" in2="SourceGraphic" operator="over"/>
    </filter>

    <!-- Emerald Arcane Bloom -->
    <filter id="plasmaGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="2.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .doom-title {{
      font-family: 'Impact', 'Arial Black', 'Franklin Gothic Heavy', sans-serif;
      letter-spacing: 2.2px;
    }}
    .ui-mono {{
      font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
    }}
    .day-label {{
      fill: #64748b;
      font-size: 9.5px;
      font-weight: 700;
      font-family: 'Fira Code', 'Consolas', monospace;
    }}
    .month-label {{
      fill: #94a3b8;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1px;
      font-family: 'Fira Code', 'Consolas', monospace;
    }}
    .dormant-cell {{
      fill: #080f0c;
      stroke: #172a22;
      stroke-width: 0.75;
    }}
    @keyframes reactorPulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.55; }}
    }}
    .reactor-pulse {{
      animation: reactorPulse 2.2s infinite ease-in-out;
    }}
    @keyframes protocolStamp {{
      0%, 62% {{ opacity: 0; }}
      69%, 92% {{ opacity: 1; }}
      98%, 100% {{ opacity: 0; }}
    }}
    .protocol-complete {{
      animation: protocolStamp {total_cycle}s infinite ease-out;
    }}
  </style>

  <!-- Outer Armored Plate Chassis -->
  <polygon points="18,2 {width-18},2 {width-2},18 {width-2},{height-18} {width-18},{height-2} 18,{height-2} 2,{height-18} 2,18"
    fill="url(#armorPlate)" stroke="#1f382d" stroke-width="2.2"/>
  <rect x="4" y="4" width="{width-8}" height="{height-8}" rx="10" fill="url(#incursionLeft)"/>
  <rect x="4" y="4" width="{width-8}" height="{height-8}" rx="10" fill="url(#incursionRight)"/>
  <rect x="4" y="4" width="{width-8}" height="{height-8}" rx="10" fill="transparent" filter="url(#steelGrain)"/>

  <!-- Inner Beveled Conduit Frame -->
  <polygon points="24,10 {width-24},10 {width-10},24 {width-10},{height-24} {width-24},{height-10} 24,{height-10} 10,{height-24} 10,24"
    fill="none" stroke="url(#energyBar)" stroke-opacity="0.38" stroke-width="1.2"/>

  <!-- Armored Plate Seam Lines & Corner Hex Bolts -->
  <g stroke="#22c55e" stroke-opacity="0.10" stroke-width="1">
    <line x1="16" y1="78" x2="{width-16}" y2="78"/>
    <line x1="16" y1="246" x2="{width-16}" y2="246"/>
    <line x1="315" y1="78" x2="315" y2="246"/>
    <line x1="628" y1="78" x2="628" y2="246"/>
  </g>
  <g fill="#1c2a24" stroke="#475569" stroke-width="1">
    <polygon points="{hex_points(24, 24)}"/>
    <polygon points="{hex_points(width-24, 24)}"/>
    <polygon points="{hex_points(24, height-24)}"/>
    <polygon points="{hex_points(width-24, height-24)}"/>
  </g>

  <!-- Subtle Multiverse Energy Fracture Cracks in Corners -->
  <g stroke="#4ade80" stroke-width="0.9" fill="none" opacity="0.28" filter="url(#plasmaGlow)">
    <polyline points="12,300 34,284 48,292 74,268"/>
    <polyline points="{width-12},295 {width-42},280 {width-58},288 {width-88},266"/>
  </g>

  <!-- ===================== DOOMSDAY TOP HUD HEADER ===================== -->
  <!-- Minimalist Vector Armored Mask / Latveria Crest Emblem (Zero Emojis) -->
  <g transform="translate(42, 18)">
    <polygon points="22,0 44,10 40,36 22,46 4,36 0,10" fill="#08120e" stroke="url(#chromeMetal)" stroke-width="1.6"/>
    <!-- Geometric Armored Brow & Glowing Emerald Eyes -->
    <path d="M 8 15 L 22 20 L 36 15 L 34 33 L 22 40 L 10 33 Z" fill="#14211b" stroke="#334155" stroke-width="0.9"/>
    <polygon points="11,21 19,23.5 18,26 11,24.5" fill="#4ade80" filter="url(#plasmaGlow)"/>
    <polygon points="33,21 25,23.5 26,26 33,24.5" fill="#4ade80" filter="url(#plasmaGlow)"/>
    <!-- Steel Respirator Grilles -->
    <line x1="16" y1="31" x2="28" y2="31" stroke="#64748b" stroke-width="1.2"/>
    <line x1="18" y1="34.5" x2="26" y2="34.5" stroke="#64748b" stroke-width="1.2"/>
  </g>

  <!-- Title & Protocol Code -->
  <text x="102" y="38" class="doom-title" font-size="21" fill="url(#chromeMetal)">DOOMSDAY ACTIVITY MATRIX</text>
  <text x="102" y="56" class="ui-mono" font-size="11" fill="#4ade80" letter-spacing="1.2">ARCANE PLASMA FORGE // EARTH-616 // @JEREMIALEX04</text>

  <!-- Top Right HUD: Multiverse Threat Meter (5 Vector Emerald Energy Bars) + Commits -->
  <g class="reactor-pulse" transform="translate({width - 210}, 20)">
    <text x="0" y="13" class="ui-mono" font-size="9.5" fill="#94a3b8" letter-spacing="1.2">ENERGY:</text>
    <rect x="58" y="3" width="18" height="10" rx="1.5" fill="#065f46" stroke="#10b981" stroke-width="0.7"/>
    <rect x="80" y="3" width="18" height="10" rx="1.5" fill="#059669" stroke="#4ade80" stroke-width="0.7"/>
    <rect x="102" y="3" width="18" height="10" rx="1.5" fill="#10b981" stroke="#86efac" stroke-width="0.7"/>
    <rect x="124" y="3" width="18" height="10" rx="1.5" fill="#22c55e" stroke="#bbf7d0" stroke-width="0.7"/>
    <rect x="146" y="3" width="18" height="10" rx="1.5" fill="#4ade80" filter="url(#plasmaGlow)"/>
  </g>
  <text x="{width - 44}" y="57" text-anchor="end" class="ui-mono" font-size="13" font-weight="700" fill="#86efac">{total_last_year} CYCLES <tspan fill="#94a3b8" font-size="10.5">// COMMITS (LAST YEAR)</tspan></text>
''')

# Month labels
for m_name, m_x in month_labels:
    svg_parts.append(f'  <text x="{m_x:.1f}" y="{grid_y0 - 11}" class="month-label">{m_name}</text>')

# Weekday labels
for d_idx, d_name in [(1, "LUN"), (3, "MIE"), (5, "VIE")]:
    y_pos = grid_y0 + d_idx * step + 9.5
    svg_parts.append(f'  <text x="22" y="{y_pos:.1f}" class="day-label">{d_name}</text>')

# 1) Dormant Armored Grid Slots
svg_parts.append('  <!-- Dormant Titanium Matrix Cells -->\n  <g id="dormant-grid">')
for w_idx, week in enumerate(weeks):
    x = grid_x0 + w_idx * step
    for d_idx, day in enumerate(week):
        if day is None:
            continue
        y = grid_y0 + d_idx * step
        svg_parts.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" class="dormant-cell"/>')
svg_parts.append('  </g>')

# 2) Progressive Plasma-Forged Columns Activated as the Emerald Scanner Sweeps
svg_parts.append('  <!-- Progressive Emerald Plasma Forged Columns -->\n  <g id="forged-layers">')

for w_idx, week in enumerate(weeks):
    x = grid_x0 + w_idx * step
    t_col = (w_idx / max(1, num_weeks - 1)) * (forge_duration / total_cycle)
    t_start = max(0.001, t_col - 0.004)
    t_mid = min(0.90, t_col + 0.015)

    key_times = f"0;{t_start:.4f};{t_mid:.4f};0.9350;0.9850;1"
    values = "0;0;1;1;0;0"

    col_elems = []
    for d_idx, day in enumerate(week):
        if day is None:
            continue
        y = grid_y0 + d_idx * step
        lvl = int(day.get("level", 0))
        cnt = int(day.get("count", 0))

        eff_lvl = 4 if cnt >= 15 else lvl
        color = level_colors.get(eff_lvl, "#10b981")

        if eff_lvl == 0:
            col_elems.append(
                f'      <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" stroke="#14261e" stroke-width="0.6" opacity="0.9"/>'
            )
        else:
            # Arcane Plasma Aura around energized cells
            if eff_lvl >= 2:
                halo_r = 9.0 if eff_lvl == 2 else (11.0 if eff_lvl == 3 else 13.0)
                col_elems.append(
                    f'      <circle cx="{x + cell_size/2:.1f}" cy="{y + cell_size/2:.1f}" r="{halo_r:.1f}" fill="{color}" opacity="0.22"/>'
                )

            glow_attr = ' filter="url(#plasmaGlow)"' if eff_lvl >= 3 else ''
            col_elems.append(
                f'      <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.2" fill="{color}" stroke="#86efac" stroke-opacity="{0.25 + eff_lvl*0.15:.2f}" stroke-width="0.7"{glow_attr}>'
                f'<title>{day["date"]}: {cnt} contribuciones</title></rect>'
            )

            # Luminous plasma core inside level 3 & 4 nodes
            if eff_lvl >= 3:
                core_c = "#dcfce7" if eff_lvl == 4 else "#86efac"
                col_elems.append(
                    f'      <rect x="{x + 3.4:.1f}" y="{y + 3.4:.1f}" width="{cell_size - 6.8:.1f}" height="{cell_size - 6.8:.1f}" rx="1.2" fill="{core_c}" opacity="0.85"/>'
                )

            # Metallic forging sparks / arcane energy embers around active nodes
            num_sparks = 2 if eff_lvl == 1 else (4 if eff_lvl == 2 else 6)
            for _ in range(num_sparks):
                dx = random.uniform(-4.0, cell_size + 4.0)
                dy = random.uniform(-4.0, cell_size + 4.0)
                r_s = random.uniform(0.55, 1.3)
                op_s = random.uniform(0.35, 0.85)
                spark_col = "#dcfce7" if (eff_lvl >= 3 and random.random() < 0.4) else color
                col_elems.append(
                    f'      <circle cx="{x + dx:.1f}" cy="{y + dy:.1f}" r="{r_s:.1f}" fill="{spark_col}" opacity="{op_s:.2f}"/>'
                )

            # Arcane energy micro-tendrils descending on peak days (levels 3 & 4)
            if eff_lvl >= 3:
                tx = x + cell_size / 2 + random.uniform(-2.5, 2.5)
                t_len = random.uniform(6.0, 14.0)
                mid_x = tx + random.uniform(-2.2, 2.2)
                col_elems.append(
                    f'      <polyline points="{tx:.1f},{y + cell_size:.1f} {mid_x:.1f},{y + cell_size + t_len*0.5:.1f} {tx:.1f},{y + cell_size + t_len:.1f}" '
                    f'fill="none" stroke="{color}" stroke-width="1.2" opacity="0.8"/>'
                )

    svg_parts.append('    <g opacity="0">')
    svg_parts.append(f'      <animate attributeName="opacity" dur="{total_cycle}s" repeatCount="indefinite" keyTimes="{key_times}" values="{values}"/>')
    svg_parts.extend(col_elems)
    svg_parts.append('    </g>')

svg_parts.append('  </g>')

# 3) Bottom Telemetry HUD, Reactor Gauge & Final Doomsday Protocol Stamp
end_x = grid_x0 + (num_weeks - 1) * step + cell_size
forge_end_ratio = forge_duration / total_cycle

svg_parts.append(f'''
  <!-- ===================== BOTTOM DOOMSDAY TELEMETRY HUD ===================== -->
  <!-- Energy Intensity Scale -->
  <g transform="translate({grid_x0}, 260)">
    <text x="0" y="11" class="ui-mono" font-size="10" fill="#94a3b8" letter-spacing="0.9">PLASMA OUTPUT:</text>
    <rect x="108" y="1" width="11" height="11" rx="2" fill="#0c1411" stroke="#1f382d"/>
    <rect x="124" y="1" width="11" height="11" rx="2" fill="#065f46"/>
    <rect x="140" y="1" width="11" height="11" rx="2" fill="#059669"/>
    <rect x="156" y="1" width="11" height="11" rx="2" fill="#10b981"/>
    <rect x="172" y="1" width="11" height="11" rx="2" fill="#4ade80" filter="url(#plasmaGlow)"/>
    <text x="192" y="11" class="ui-mono" font-size="10" fill="#4ade80" letter-spacing="0.9">INCURSION PEAK</text>
  </g>

  <!-- Live Sync Progress Bar -->
  <g transform="translate({width - 310}, 262)">
    <text x="0" y="9" class="ui-mono" font-size="10" fill="#94a3b8" letter-spacing="0.9">FORGE SYNC:</text>
    <rect x="82" y="0" width="186" height="10" rx="4" fill="#070e0b" stroke="#1f382d"/>
    <rect x="82" y="0" width="0" height="10" rx="4" fill="url(#energyBar)" filter="url(#plasmaGlow)">
      <animate attributeName="width" dur="{total_cycle}s" repeatCount="indefinite"
        keyTimes="0;{forge_end_ratio:.4f};0.935;0.985;1"
        values="0;186;186;0;0"/>
    </rect>
  </g>

  <!-- Final Illuminated Protocol Stamp -->
  <g class="protocol-complete">
    <text x="{width/2:.1f}" y="311" text-anchor="middle" class="doom-title" font-size="22" fill="url(#chromeMetal)" stroke="#040706" stroke-width="0.9" letter-spacing="4" filter="url(#plasmaGlow)">
      DOOMSDAY PROTOCOL  //  MATRIX ONLINE
    </text>
    <rect x="{width/2 - 170:.1f}" y="319" width="340" height="2" fill="url(#energyBar)" opacity="0.9"/>
  </g>
''')

# 4) Animated Arcane Emerald Plasma Forging Scanner Sweeping Across the Matrix
start_x = grid_x0
beam_top = grid_y0 - 12
beam_h = 7 * step + 20

svg_parts.append(f'''
  <!-- ===================== ANIMATED ARCANE PLASMA FORGING RIG ===================== -->
  <g id="doomsday-scanner-rig">
    <!-- Horizontal sweep across all 53 weeks -->
    <animateTransform attributeName="transform" type="translate" dur="{total_cycle}s" repeatCount="indefinite"
      keyTimes="0;{forge_end_ratio:.4f};0.95;1"
      values="{start_x} {beam_top}; {end_x} {beam_top}; {end_x + 24} {beam_top}; {start_x} {beam_top}"/>

    <!-- Visibility envelope -->
    <animate attributeName="opacity" dur="{total_cycle}s" repeatCount="indefinite"
      keyTimes="0;0.015;{forge_end_ratio - 0.01:.4f};{forge_end_ratio + 0.03:.4f};0.98;1"
      values="0;1;1;0;0;0"/>

    <!-- Vertical Plasma Curtain Beam -->
    <rect x="-14" y="0" width="28" height="{beam_h:.1f}" fill="url(#plasmaBeamH)"/>
    <line x1="0" y1="0" x2="0" y2="{beam_h:.1f}" stroke="#ecfdf5" stroke-width="1.8" filter="url(#plasmaGlow)"/>

    <!-- Top & Bottom Armored Titanium Emitter Rail Clamps -->
    <polygon points="-9,-6 9,-6 6,3 -6,3" fill="url(#chromeMetal)" stroke="#040706" stroke-width="0.8"/>
    <rect x="-4" y="1" width="8" height="3" fill="#4ade80" filter="url(#plasmaGlow)"/>
    <polygon points="-6,{beam_h - 3:.1f} 6,{beam_h - 3:.1f} 9,{beam_h + 6:.1f} -9,{beam_h + 6:.1f}" fill="url(#chromeMetal)" stroke="#040706" stroke-width="0.8"/>
    <rect x="-4" y="{beam_h - 4:.1f}" width="8" height="3" fill="#4ade80" filter="url(#plasmaGlow)"/>

    <!-- Rapid Vertical Plasma Focusing Node & Spark Burst -->
    <g>
      <animateTransform attributeName="transform" type="translate" dur="0.48s" repeatCount="indefinite"
        values="0 14; 0 {beam_h - 18:.1f}; 0 14"/>

      <circle cx="0" cy="0" r="24" fill="url(#plasmaImpact)"/>
      <circle cx="0" cy="0" r="6" fill="#ecfdf5" filter="url(#plasmaGlow)"/>

      <!-- Arcane Geometric Diamond Reticle -->
      <polygon points="0,-11 11,0 0,11 -11,0" fill="none" stroke="#86efac" stroke-width="1" opacity="0.85"/>

      <!-- Flying Forging Sparks -->
      <circle cx="-13" cy="-9" r="1.6" fill="#4ade80" opacity="0.9"/>
      <circle cx="-18" cy="6" r="1.3" fill="#dcfce7" opacity="0.85"/>
      <circle cx="-9" cy="14" r="1.5" fill="#10b981" opacity="0.8"/>
      <circle cx="10" cy="-12" r="1.2" fill="#86efac" opacity="0.8"/>
      <circle cx="14" cy="9" r="1.4" fill="#4ade80" opacity="0.75"/>
      <line x1="-2" y1="-2" x2="-15" y2="-11" stroke="#86efac" stroke-width="0.9" opacity="0.7"/>
      <line x1="-2" y1="3" x2="-16" y2="12" stroke="#4ade80" stroke-width="0.9" opacity="0.65"/>
    </g>
  </g>
</svg>
''')

with open("public/doomsday-activity-board.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))

print(f"Generated Avengers: Doomsday SVG headers + public/doomsday-activity-board.svg ({num_weeks} weeks, {total_last_year} contributions).")
