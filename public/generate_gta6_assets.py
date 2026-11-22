import html
import json
import math
import random
import urllib.request
from datetime import datetime

random.seed(2026)

# ---------------------------------------------------------
# 1. Generate realistic GTA VI Section Headers (Zero Emojis)
# ---------------------------------------------------------
def create_section_header(filename, kicker, title, accent_left="#ff2a85", accent_right="#00f0ff"):
    kicker_xml = html.escape(kicker)
    title_xml = html.escape(title)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 74" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d0718" stop-opacity="0"/>
      <stop offset="15%" stop-color="#140924" stop-opacity="0.95"/>
      <stop offset="85%" stop-color="#140924" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#0d0718" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="neonLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_left}" stop-opacity="0"/>
      <stop offset="20%" stop-color="{accent_left}"/>
      <stop offset="50%" stop-color="#ff9e44"/>
      <stop offset="80%" stop-color="{accent_right}"/>
      <stop offset="100%" stop-color="{accent_right}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="textSunset" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#ffe4f2"/>
      <stop offset="100%" stop-color="#a5f3fc"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="6" width="920" height="62" fill="url(#bgGrad)"/>

  <!-- Top and bottom neon accent lines -->
  <rect x="40" y="6" width="840" height="2" fill="url(#neonLine)" filter="url(#glow)"/>
  <rect x="110" y="66" width="700" height="1.5" fill="url(#neonLine)" opacity="0.7"/>

  <!-- Geometric Vice City corner brackets -->
  <path d="M 65 18 L 50 18 L 50 56 L 65 56" fill="none" stroke="{accent_left}" stroke-width="2" opacity="0.85"/>
  <path d="M 855 18 L 870 18 L 870 56 L 855 56" fill="none" stroke="{accent_right}" stroke-width="2" opacity="0.85"/>

  <!-- Subtle vector chevron markers -->
  <polygon points="82,37 92,31 92,43" fill="{accent_left}" opacity="0.8"/>
  <polygon points="838,37 828,31 828,43" fill="{accent_right}" opacity="0.8"/>

  <!-- Kicker -->
  <text x="460" y="26" text-anchor="middle" font-family="'Segoe UI', 'Montserrat', 'Arial', sans-serif" font-size="10.5" font-weight="700" letter-spacing="4.5" fill="#ff7b54">{kicker_xml}</text>

  <!-- Main Title -->
  <text x="460" y="54" text-anchor="middle" font-family="'Impact', 'Arial Black', 'Franklin Gothic Heavy', sans-serif" font-size="25" letter-spacing="3" fill="url(#textSunset)" filter="url(#glow)">{title_xml}</text>
</svg>
'''
    with open(f"public/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)

create_section_header("gta6-header-specialties.svg", "LEONIDA OPERATIONS // CORE FOCUS", "SPECIALTIES & ARCHITECTURE")
create_section_header("gta6-header-stack.svg", "VICE CITY LOADOUT // TECHNOLOGIES", "ARSENAL & TECH STACK")
create_section_header("gta6-header-stats.svg", "TELEMETRY // PROFILE ANALYTICS", "VICE CITY RECORD & STATS")
create_section_header("gta6-header-activity.svg", "OCEAN BEACH CONCRETE WALL // LIVE DATA", "AEROSOL ACTIVITY BOARD")

# ---------------------------------------------------------
# 2. Generate Realistic GTA VI Aerosol Spray Activity SVG
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
height = 340
grid_x0 = 62
grid_y0 = 108
cell_size = 12.2
cell_gap = 3.6
step = cell_size + cell_gap

spray_duration = 10.0
hold_duration = 5.5
total_cycle = spray_duration + hold_duration

# GTA VI Vice City Neon Aerosol Palette
level_colors = {
    0: "#1a1128",
    1: "#7b2cbf",  # Deep Vice Violet spray
    2: "#e11d74",  # Vice Magenta spray
    3: "#ff6b4a",  # Leonida Sunset Coral spray
    4: "#00f0ff",  # Electric Miami Cyan highlight
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

# Helper for vector 5-pointed star (zero emoji)
def star_polygon(cx, cy, r_outer=7.5, r_inner=3.2):
    pts = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
    return " ".join(pts)

stars_svg = []
for i in range(5):
    cx = (width - 148) + i * 24
    stars_svg.append(
        f'    <polygon points="{star_polygon(cx, 32, 8.2, 3.5)}" fill="url(#viSunset)" stroke="#0b0614" stroke-width="0.9" filter="url(#neonGlow)"/>'
    )

svg_parts = []
svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <!-- Concrete Wall Night Gradient -->
    <linearGradient id="wallBase" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0614"/>
      <stop offset="45%" stop-color="#130a22"/>
      <stop offset="100%" stop-color="#090b16"/>
    </linearGradient>

    <!-- Ambient Vice City Street Neon Spill (Magenta Left + Cyan Right) -->
    <radialGradient id="neonSpillLeft" cx="12%" cy="18%" r="48%">
      <stop offset="0%" stop-color="#ff2a85" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="#7b2cbf" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0b0614" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="neonSpillRight" cx="88%" cy="82%" r="45%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.18"/>
      <stop offset="60%" stop-color="#1d4ed8" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#090b16" stop-opacity="0"/>
    </radialGradient>

    <!-- Iconic GTA VI Sunset Gradient -->
    <linearGradient id="viSunset" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ff2a85"/>
      <stop offset="48%" stop-color="#ff7b54"/>
      <stop offset="100%" stop-color="#ffd166"/>
    </linearGradient>

    <linearGradient id="viBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7b2cbf"/>
      <stop offset="35%" stop-color="#ff2a85"/>
      <stop offset="70%" stop-color="#ff7b54"/>
      <stop offset="100%" stop-color="#00f0ff"/>
    </linearGradient>

    <!-- 3D Metallic Aerosol Can Body Gradient -->
    <linearGradient id="canMetal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e1b2e"/>
      <stop offset="28%" stop-color="#4c4668"/>
      <stop offset="55%" stop-color="#151221"/>
      <stop offset="85%" stop-color="#2e2845"/>
      <stop offset="100%" stop-color="#0d0a16"/>
    </linearGradient>
    <linearGradient id="canChrome" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b"/>
      <stop offset="35%" stop-color="#f8fafc"/>
      <stop offset="65%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>

    <!-- Realistic Pressurized Aerosol Mist -->
    <radialGradient id="mistOuter" cx="35%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#ff7b54" stop-opacity="0.72"/>
      <stop offset="35%" stop-color="#ff2a85" stop-opacity="0.45"/>
      <stop offset="72%" stop-color="#7b2cbf" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sprayCone" x1="100%" y1="50%" x2="0%" y2="50%">
      <stop offset="0%" stop-color="#fff1f2" stop-opacity="0.92"/>
      <stop offset="22%" stop-color="#ff7b54" stop-opacity="0.65"/>
      <stop offset="62%" stop-color="#ff2a85" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#00f0ff" stop-opacity="0"/>
    </linearGradient>

    <!-- Concrete Stucco Wall Texture Filter -->
    <filter id="concreteTex" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" seed="11" result="noise"/>
      <feColorMatrix type="matrix" values="
        0 0 0 0 0.75
        0 0 0 0 0.65
        0 0 0 0 0.90
        0 0 0 0.055 0" in="noise" result="coloredNoise"/>
      <feComposite in="coloredNoise" in2="SourceGraphic" operator="over"/>
    </filter>

    <!-- Organic Aerosol Overspray Edge Filter -->
    <filter id="sprayTexture" x="-25%" y="-25%" width="150%" height="150%">
      <feTurbulence type="fractalNoise" baseFrequency="0.42" numOctaves="2" seed="7" result="grain"/>
      <feDisplacementMap in="SourceGraphic" in2="grain" scale="1.7" xChannelSelector="R" yChannelSelector="G" result="rough"/>
      <feGaussianBlur in="rough" stdDeviation="0.9" result="soft"/>
      <feMerge>
        <feMergeNode in="soft"/>
        <feMergeNode in="rough"/>
      </feMerge>
    </filter>

    <!-- Neon Bloom Glow -->
    <filter id="neonGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Clip Path for Palm Silhouette inside VI Emblem -->
    <clipPath id="viBadgeClip">
      <rect x="0" y="0" width="54" height="44" rx="5"/>
    </clipPath>
  </defs>

  <style>
    .hud-title {{
      font-family: 'Impact', 'Arial Black', 'Franklin Gothic Heavy', sans-serif;
      letter-spacing: 1.8px;
    }}
    .ui-sans {{
      font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }}
    .ui-mono {{
      font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
    }}
    .day-label {{
      fill: #94a3b8;
      font-size: 9.5px;
      font-weight: 600;
      font-family: 'Fira Code', 'Consolas', monospace;
    }}
    .month-label {{
      fill: #cbd5e1;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      font-family: 'Fira Code', 'Consolas', monospace;
    }}
    .stencil-cell {{
      fill: #120b1f;
      stroke: #26193d;
      stroke-width: 0.75;
    }}
    @keyframes wantedPulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.7; }}
    }}
    .wanted-group {{
      animation: wantedPulse 2.4s infinite ease-in-out;
    }}
    @keyframes passStamp {{
      0%, 63% {{ opacity: 0; }}
      69%, 92% {{ opacity: 1; }}
      98%, 100% {{ opacity: 0; }}
    }}
    .mission-stamp {{
      animation: passStamp {total_cycle}s infinite ease-out;
    }}
  </style>

  <!-- Concrete Wall Surface & Ambient Street Neon Reflections -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="12" fill="url(#wallBase)" stroke="#2e1d4a" stroke-width="2"/>
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="12" fill="url(#neonSpillLeft)"/>
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="12" fill="url(#neonSpillRight)"/>
  <rect x="4" y="4" width="{width-8}" height="{height-8}" rx="10" fill="transparent" filter="url(#concreteTex)"/>

  <!-- Subtle Wall Concrete Seams & Architectural Plaster Joints -->
  <g stroke="#ffffff" stroke-opacity="0.035" stroke-width="1">
    <line x1="14" y1="76" x2="{width-14}" y2="76"/>
    <line x1="14" y1="242" x2="{width-14}" y2="242"/>
    <line x1="315" y1="76" x2="315" y2="242"/>
    <line x1="630" y1="76" x2="630" y2="242"/>
  </g>

  <!-- Subtle Palm Frond Shadows Projected onto Concrete Wall Corners -->
  <g fill="#05020a" opacity="0.45">
    <path d="M 10 330 Q 45 270 95 255 Q 60 282 40 330 Z"/>
    <path d="M 10 295 Q 55 255 110 268 Q 62 275 18 310 Z"/>
    <path d="M {width-10} 330 Q {width-50} 260 {width-110} 248 Q {width-62} 280 {width-35} 330 Z"/>
    <path d="M {width-10} 290 Q {width-60} 245 {width-125} 260 Q {width-70} 268 {width-20} 305 Z"/>
  </g>

  <!-- Neon Outer Accent Border -->
  <rect x="9" y="9" width="{width-18}" height="{height-18}" rx="8" fill="none" stroke="url(#viBar)" stroke-opacity="0.42" stroke-width="1.2"/>

  <!-- ===================== GTA VI TOP HUD BAR ===================== -->
  <!-- Authentic-style VI Emblem -->
  <g transform="translate(24, 18)">
    <rect x="0" y="0" width="54" height="44" rx="5" fill="#090512" stroke="url(#viBar)" stroke-width="1.6"/>
    <g clip-path="url(#viBadgeClip)">
      <!-- Sunset Glow inside Badge -->
      <circle cx="27" cy="40" r="24" fill="url(#viSunset)" opacity="0.22"/>
      <!-- Roman Numeral VI -->
      <text x="27" y="34" text-anchor="middle" class="hud-title" font-size="31" fill="url(#viSunset)" stroke="#090512" stroke-width="1.1">VI</text>
      <!-- Tiny Palm Silhouette Overlay -->
      <path d="M 12 44 Q 16 32 21 26 M 21 26 Q 14 23 10 27 M 21 26 Q 27 21 31 26 M 21 26 Q 25 27 28 32" stroke="#090512" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    </g>
  </g>

  <!-- Wall Header Typography -->
  <text x="92" y="37" class="hud-title" font-size="21" fill="#f8fafc">VICE CITY STREET WALL</text>
  <text x="92" y="55" class="ui-mono" font-size="11" fill="#ff7b54" letter-spacing="1.2">LEONIDA AEROSOL CONTRIBUTION LOG // @JEREMIALEX04</text>

  <!-- Top Right HUD: Vector Wanted Stars + Total Commits Cash Readout -->
  <g class="wanted-group">
{chr(10).join(stars_svg)}
  </g>
  <text x="{width - 26}" y="57" text-anchor="end" class="ui-mono" font-size="13.5" font-weight="700" fill="#00f0ff">${total_last_year:,},000 <tspan fill="#e2e8f0" font-size="10.5">// {total_last_year} COMMITS (LAST YEAR)</tspan></text>
''')

# Month labels
for m_name, m_x in month_labels:
    svg_parts.append(f'  <text x="{m_x:.1f}" y="{grid_y0 - 11}" class="month-label">{m_name}</text>')

# Weekday labels
for d_idx, d_name in [(1, "LUN"), (3, "MIE"), (5, "VIE")]:
    y_pos = grid_y0 + d_idx * step + 9.5
    svg_parts.append(f'  <text x="22" y="{y_pos:.1f}" class="day-label">{d_name}</text>')

# 1) Unpainted Concrete Stencil Slots
svg_parts.append('  <!-- Concrete Stencil Base Grid -->\n  <g id="stencil-grid">')
for w_idx, week in enumerate(weeks):
    x = grid_x0 + w_idx * step
    for d_idx, day in enumerate(week):
        if day is None:
            continue
        y = grid_y0 + d_idx * step
        svg_parts.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.2" class="stencil-cell"/>')
svg_parts.append('  </g>')

# 2) Spray-Painted Contribution Columns (Revealed Synchronized with Aerosol Pass)
svg_parts.append('  <!-- Progressive Aerosol Spray-Painted Columns -->\n  <g id="sprayed-layers">')

for w_idx, week in enumerate(weeks):
    x = grid_x0 + w_idx * step
    t_col = (w_idx / max(1, num_weeks - 1)) * (spray_duration / total_cycle)
    t_start = max(0.001, t_col - 0.004)
    t_mid = min(0.90, t_col + 0.014)

    key_times = f"0;{t_start:.4f};{t_mid:.4f};0.9350;0.9850;1"
    values = "0;0;1;1;0;0"

    col_elems = []
    for d_idx, day in enumerate(week):
        if day is None:
            continue
        y = grid_y0 + d_idx * step
        lvl = int(day.get("level", 0))
        cnt = int(day.get("count", 0))

        # Elevate very high commit days (>=15) to level 4 electric cyan accent
        eff_lvl = 4 if cnt >= 15 else lvl
        color = level_colors.get(eff_lvl, "#ff2a85")

        if eff_lvl == 0:
            col_elems.append(
                f'      <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.4" fill="{color}" opacity="0.82"/>'
            )
        else:
            # Soft overspray halo beneath the painted square
            halo_r = 7.5 if eff_lvl == 1 else (9.5 if eff_lvl == 2 else 11.5)
            col_elems.append(
                f'      <circle cx="{x + cell_size/2:.1f}" cy="{y + cell_size/2:.1f}" r="{halo_r:.1f}" fill="{color}" opacity="0.22"/>'
            )
            # Painted square with rough aerosol texture
            filt = ' filter="url(#sprayTexture)"' if eff_lvl >= 2 else ''
            col_elems.append(
                f'      <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.8" fill="{color}"{filt}>'
                f'<title>{day["date"]}: {cnt} contribuciones</title></rect>'
            )
            # Subtle wet-paint specular highlight on top edge
            col_elems.append(
                f'      <line x1="{x + 2.2:.1f}" y1="{y + 2.2:.1f}" x2="{x + cell_size - 3:.1f}" y2="{y + 2.2:.1f}" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1" stroke-linecap="round"/>'
            )

            # Fine aerosol atomized splatter particles around the cell
            num_dots = 3 if eff_lvl == 1 else (5 if eff_lvl == 2 else 8)
            for _ in range(num_dots):
                dx = random.uniform(-4.5, cell_size + 4.5)
                dy = random.uniform(-4.5, cell_size + 4.5)
                r_dot = random.uniform(0.55, 1.45)
                dot_op = random.uniform(0.35, 0.85)
                col_elems.append(
                    f'      <circle cx="{x + dx:.1f}" cy="{y + dy:.1f}" r="{r_dot:.1f}" fill="{color}" opacity="{dot_op:.2f}"/>'
                )

            # Realistic paint drips on heavy spray cells (levels 3 & 4, and some level 2)
            if eff_lvl >= 3 or (eff_lvl == 2 and random.random() < 0.30):
                drip_x = x + random.uniform(2.5, cell_size - 2.5)
                drip_len = random.uniform(7.0, 17.5) if eff_lvl >= 3 else random.uniform(4.0, 8.5)
                col_elems.append(
                    f'      <path d="M {drip_x:.1f} {y + cell_size - 1:.1f} L {drip_x:.1f} {y + cell_size + drip_len:.1f}" '
                    f'stroke="{color}" stroke-width="1.7" stroke-linecap="round" opacity="0.88"/>'
                )
                col_elems.append(
                    f'      <circle cx="{drip_x:.1f}" cy="{y + cell_size + drip_len:.1f}" r="1.55" fill="{color}" opacity="0.95"/>'
                )
                # Tiny white glossy wet highlight on the droplet
                col_elems.append(
                    f'      <circle cx="{drip_x - 0.4:.1f}" cy="{y + cell_size + drip_len - 0.4:.1f}" r="0.45" fill="#ffffff" opacity="0.7"/>'
                )

    svg_parts.append('    <g opacity="0">')
    svg_parts.append(f'      <animate attributeName="opacity" dur="{total_cycle}s" repeatCount="indefinite" keyTimes="{key_times}" values="{values}"/>')
    svg_parts.extend(col_elems)
    svg_parts.append('    </g>')

svg_parts.append('  </g>')

# 3) Bottom HUD Legend, Spray Progress Bar & Mission Passed Neon Tag
end_x = grid_x0 + (num_weeks - 1) * step + cell_size
spray_end_ratio = spray_duration / total_cycle

svg_parts.append(f'''
  <!-- ===================== BOTTOM VICE CITY HUD ===================== -->
  <!-- Aerosol Intensity Legend -->
  <g transform="translate({grid_x0}, 256)">
    <text x="0" y="11" class="ui-mono" font-size="10" fill="#94a3b8" letter-spacing="0.8">SPRAY DENSITY:</text>
    <rect x="108" y="1" width="11" height="11" rx="2.2" fill="#1a1128" stroke="#2e1d4a"/>
    <rect x="124" y="1" width="11" height="11" rx="2.2" fill="#7b2cbf"/>
    <rect x="140" y="1" width="11" height="11" rx="2.2" fill="#e11d74"/>
    <rect x="156" y="1" width="11" height="11" rx="2.2" fill="#ff6b4a"/>
    <rect x="172" y="1" width="11" height="11" rx="2.2" fill="#00f0ff" filter="url(#neonGlow)"/>
    <text x="192" y="11" class="ui-mono" font-size="10" fill="#00f0ff" letter-spacing="0.8">OVERDRIVE</text>
  </g>

  <!-- Live Aerosol Progress Gauge -->
  <g transform="translate({width - 295}, 258)">
    <text x="0" y="9" class="ui-mono" font-size="10" fill="#94a3b8" letter-spacing="0.8">COVERAGE:</text>
    <rect x="72" y="0" width="190" height="10" rx="5" fill="#120b1f" stroke="#2e1d4a"/>
    <rect x="72" y="0" width="0" height="10" rx="5" fill="url(#viBar)" filter="url(#neonGlow)">
      <animate attributeName="width" dur="{total_cycle}s" repeatCount="indefinite"
        keyTimes="0;{spray_end_ratio:.4f};0.935;0.985;1"
        values="0;190;190;0;0"/>
    </rect>
  </g>

  <!-- Vice City Mission Passed Neon Graffiti Signature -->
  <g class="mission-stamp">
    <text x="{width/2:.1f}" y="306" text-anchor="middle" class="hud-title" font-size="23" fill="url(#viSunset)" stroke="#090512" stroke-width="1" letter-spacing="3.5" filter="url(#neonGlow)">
      MISSION PASSED  //  RESPECT +
    </text>
    <rect x="{width/2 - 140:.1f}" y="314" width="280" height="2" fill="url(#viBar)" opacity="0.85"/>
  </g>
''')

# 4) Hyper-Detailed Animated Aerosol Spray Can + Pressurized Cone & Atomized Cloud
start_x = grid_x0

svg_parts.append(f'''
  <!-- ===================== REALISTIC ANIMATED AEROSOL SPRAY CAN ===================== -->
  <g id="aerosol-can-rig">
    <!-- Horizontal sweep across all 53 weeks -->
    <animateTransform attributeName="transform" type="translate" dur="{total_cycle}s" repeatCount="indefinite"
      keyTimes="0;{spray_end_ratio:.4f};0.95;1"
      values="{start_x} {grid_y0}; {end_x} {grid_y0}; {end_x + 28} {grid_y0}; {start_x} {grid_y0}"/>

    <!-- Visibility envelope (appears on sweep, fades smoothly when finished) -->
    <animate attributeName="opacity" dur="{total_cycle}s" repeatCount="indefinite"
      keyTimes="0;0.015;{spray_end_ratio - 0.01:.4f};{spray_end_ratio + 0.03:.4f};0.98;1"
      values="0;1;1;0;0;0"/>

    <!-- Fast wrist up-and-down spraying oscillation -->
    <g>
      <animateTransform attributeName="transform" type="translate" dur="0.42s" repeatCount="indefinite"
        values="0 4; 0 88; 0 4"/>

      <!-- Pressurized Atomized Mist Hitting Concrete Wall -->
      <circle cx="-2" cy="8" r="28" fill="url(#mistOuter)"/>
      <circle cx="-6" cy="4" r="14" fill="#ff7b54" opacity="0.32" filter="url(#neonGlow)"/>
      <circle cx="0" cy="8" r="7" fill="#fff1f2" opacity="0.45"/>

      <!-- Dynamic Atomized Droplet Cloud -->
      <g>
        <circle cx="-15" cy="-10" r="1.8" fill="#00f0ff" opacity="0.85"/>
        <circle cx="-11" cy="18" r="1.6" fill="#ff2a85" opacity="0.85"/>
        <circle cx="6" cy="-13" r="1.4" fill="#ffd166" opacity="0.8"/>
        <circle cx="-20" cy="4" r="1.2" fill="#ff7b54" opacity="0.85"/>
        <circle cx="-5" cy="-16" r="1.1" fill="#ff2a85" opacity="0.75"/>
        <circle cx="4" cy="21" r="1.5" fill="#00f0ff" opacity="0.75"/>
        <circle cx="-17" cy="14" r="1.0" fill="#ffd166" opacity="0.7"/>
      </g>

      <!-- High-Pressure Spray Fan Cone -->
      <polygon points="29,12 -4,-13 -4,26" fill="url(#sprayCone)"/>

      <!-- 3D Detailed Aerosol Can Tilted in Hand Position -->
      <g transform="translate(28, 12) rotate(-25)">
        <!-- White Cap & Pressurized Nozzle -->
        <rect x="6" y="-8.5" width="9" height="6.5" rx="1.2" fill="#f8fafc" stroke="#0f172a" stroke-width="0.9"/>
        <rect x="5" y="-6.8" width="2.4" height="2.4" rx="0.5" fill="#ff2a85"/>
        <!-- Nozzle Depression Collar -->
        <rect x="4" y="-2.2" width="13" height="2.2" rx="0.8" fill="#cbd5e1" stroke="#0f172a" stroke-width="0.6"/>
        <!-- Brushed Chrome Shoulder Dome -->
        <path d="M 1.5 3.5 Q 10.5 -4.5 19.5 3.5 Z" fill="url(#canChrome)" stroke="#0f172a" stroke-width="0.9"/>
        <rect x="0.5" y="2.8" width="20" height="3" rx="1.2" fill="url(#canChrome)" stroke="#0f172a" stroke-width="0.8"/>
        <!-- Cylindrical Body with Metallic Shading -->
        <rect x="0.5" y="5.5" width="20" height="40" rx="2" fill="url(#canMetal)" stroke="#ff2a85" stroke-width="1"/>
        <!-- Glossy Vertical Highlight -->
        <rect x="4.5" y="6.5" width="3" height="38" fill="#ffffff" opacity="0.16"/>
        <!-- Vice City VI Label Band -->
        <rect x="1.5" y="12" width="18" height="22" fill="url(#viSunset)"/>
        <rect x="1.5" y="12" width="18" height="3" fill="#090512" opacity="0.65"/>
        <rect x="1.5" y="31" width="18" height="3" fill="#00f0ff" opacity="0.85"/>
        <text x="10.5" y="27.5" text-anchor="middle" class="hud-title" font-size="13" fill="#090512">VI</text>
        <!-- Bottom Crimped Metal Rim -->
        <rect x="0.5" y="45" width="20" height="3.2" rx="1.2" fill="url(#canChrome)" stroke="#0f172a" stroke-width="0.8"/>
      </g>
    </g>
  </g>
</svg>
''')

with open("public/gta6-spray-contributions.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))

print(f"Generated GTA VI SVG headers + public/gta6-spray-contributions.svg ({num_weeks} weeks, {total_last_year} contributions).")
