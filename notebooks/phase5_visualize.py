# ============================================================
# PHASE 5 — Build Charts & Insights
# Creates 6 publication-quality charts saved to charts/
# Uses matplotlib + seaborn 
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')   # Non-interactive backend — works without a display
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('charts', exist_ok=True)

# ------ Shared style -------------------------------------------
plt.rcParams.update({
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.grid':         True,
    'grid.color':        '#e8e8e8',
    'grid.linewidth':    0.6,
    'font.family':       'DejaVu Sans',
    'font.size':         11,
})

TEAL    = '#1D9E75'
CORAL   = '#D85A30'
PURPLE  = '#534AB7'
GRAY    = '#888780'
AMBER   = '#BA7517'
BLUE    = '#185FA5'
COLORS6 = [TEAL, TEAL, TEAL, TEAL, TEAL, CORAL]  # Last bar highlighted

print("Loading data files...")
funnel_df  = pd.read_csv('data/funnel_summary.csv')
device_df  = pd.read_csv('data/device_funnel.csv')
channel_df = pd.read_csv('data/channel_funnel.csv')
monthly_df = pd.read_csv('data/monthly_trend.csv')
opp_df     = pd.read_csv('data/revenue_opportunity.csv').iloc[0]
df         = pd.read_csv('data/clean_funnel_data.csv')

print("Generating charts...")

# ==============================================================
# CHART 1 — Funnel Bar Chart (horizontal)
# ==============================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(
    funnel_df['label'][::-1],
    funnel_df['users'][::-1],
    color=COLORS6[::-1],
    height=0.55,
    edgecolor='none',
)

# Annotate each bar
for bar, (_, row) in zip(bars, funnel_df[::-1].iterrows()):
    ax.text(
        bar.get_width() + 80,
        bar.get_y() + bar.get_height() / 2,
        f"{row['users']:,}  ({row['overall_rate']}%)",
        va='center', fontsize=10, color='#444441',
    )

ax.set_xlabel('Number of Users', labelpad=10)
ax.set_title('SaaS Signup-to-Paid Funnel\nOverall conversion: 2.8%', fontsize=14, pad=15)
ax.set_xlim(0, funnel_df['users'].max() * 1.25)
ax.tick_params(axis='y', length=0)

plt.tight_layout()
plt.savefig('charts/01_funnel_overview.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: charts/01_funnel_overview.png")

# ==============================================================
# CHART 2 — Step-by-step conversion rate (bar)
# ==============================================================
fig, ax = plt.subplots(figsize=(10, 5))

step_data  = funnel_df.iloc[1:]   # Skip stage 1 (always 100%)
step_colors = [CORAL if r < 50 else TEAL for r in step_data['step_rate']]

bars = ax.bar(
    range(len(step_data)),
    step_data['step_rate'],
    color=step_colors,
    edgecolor='none',
    width=0.55,
)

for bar, val in zip(bars, step_data['step_rate']):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        f'{val:.1f}%',
        ha='center', fontsize=10,
    )

ax.set_xticks(range(len(step_data)))
ax.set_xticklabels(step_data['label'], rotation=20, ha='right')
ax.set_ylabel('Conversion Rate (%)')
ax.set_title('Step-by-Step Conversion Rates\n(red = below 50% — needs attention)', fontsize=13, pad=12)
ax.set_ylim(0, 100)
ax.axhline(50, color=CORAL, linewidth=1, linestyle='--', alpha=0.5, label='50% threshold')
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('charts/02_step_conversion.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: charts/02_step_conversion.png")

# ==============================================================
# CHART 3 — Device comparison (grouped bars)
# ==============================================================
PAID_STAGE = 'Converted to Paid'
paid_device = device_df[device_df['stage'] == PAID_STAGE].copy()
paid_device = paid_device.sort_values('rate', ascending=False)

fig, ax = plt.subplots(figsize=(7, 5))
bar_colors = [TEAL if d == 'desktop' else CORAL if d == 'mobile' else AMBER
              for d in paid_device['device']]

bars = ax.bar(paid_device['device'], paid_device['rate'],
              color=bar_colors, edgecolor='none', width=0.45)

for bar, val in zip(bars, paid_device['rate']):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f'{val:.1f}%', ha='center', fontsize=11)

ax.set_ylabel('Paid Conversion Rate (%)')
ax.set_title('Conversion to Paid by Device\n Mobile is 7x worse than desktop', fontsize=13, pad=12)
ax.set_ylim(0, paid_device['rate'].max() * 1.4)

# Annotation arrow pointing at mobile bar
mobile_x = list(paid_device['device']).index('mobile')
ax.annotate(
    'Mobile problem!',
    xy=(mobile_x, paid_device[paid_device['device']=='mobile']['rate'].values[0]),
    xytext=(mobile_x + 0.6, paid_device['rate'].max() * 0.6),
    arrowprops=dict(arrowstyle='->', color=CORAL, lw=1.5),
    color=CORAL, fontsize=10,
)

plt.tight_layout()
plt.savefig('charts/03_device_conversion.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: charts/03_device_conversion.png")

# ==============================================================
# CHART 4 — Channel performance (horizontal bar)
# ==============================================================
paid_channel = channel_df[channel_df['stage'] == PAID_STAGE].copy()
paid_channel = paid_channel[paid_channel['channel'] != 'unknown']
paid_channel = paid_channel.sort_values('rate')

fig, ax = plt.subplots(figsize=(9, 5))
ch_colors = [TEAL if r >= paid_channel['rate'].median() else CORAL for r in paid_channel['rate']]

bars = ax.barh(paid_channel['channel'], paid_channel['rate'],
               color=ch_colors, edgecolor='none', height=0.5)

for bar, val in zip(bars, paid_channel['rate']):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=10)

ax.set_xlabel('Paid Conversion Rate (%)')
ax.set_title('Conversion to Paid by Channel\nReferral leads — paid ads underperform', fontsize=13, pad=12)
ax.set_xlim(0, paid_channel['rate'].max() * 1.3)
ax.tick_params(axis='y', length=0)

plt.tight_layout()
plt.savefig('charts/04_channel_conversion.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: charts/04_channel_conversion.png")

# ==============================================================
# CHART 5 — Monthly revenue trend (line + bar combo)
# ==============================================================
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.bar(monthly_df['signup_month'], monthly_df['revenue'],
        color=TEAL, alpha=0.35, edgecolor='none', label='Revenue ($)')
ax1.set_ylabel('Monthly Revenue ($)', color=TEAL)
ax1.tick_params(axis='y', labelcolor=TEAL)

ax2 = ax1.twinx()
ax2.plot(monthly_df['signup_month'], monthly_df['cvr'],
         color=CORAL, marker='o', linewidth=2, markersize=6, label='CVR (%)')
ax2.set_ylabel('Conversion Rate (%)', color=CORAL)
ax2.tick_params(axis='y', labelcolor=CORAL)

ax1.set_title('Monthly Revenue & Conversion Rate Trend', fontsize=13, pad=12)
ax1.set_xlabel('')
plt.xticks(rotation=20, ha='right')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('charts/05_monthly_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: charts/05_monthly_trend.png")

# ==============================================================
# CHART 6 — Revenue opportunity (before vs after fixing mobile)
# ==============================================================
fig, ax = plt.subplots(figsize=(7, 5))

current_rev   = df['monthly_revenue'].sum()
potential_rev = current_rev + opp_df['extra_monthly_revenue']
labels        = ['Current Revenue', 'Potential Revenue\n(if mobile fixed)']
values        = [current_rev, potential_rev]
colors        = [GRAY, TEAL]

bars = ax.bar(labels, values, color=colors, edgecolor='none', width=0.45)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 200,
            f'${val:,.0f}/mo', ha='center', fontsize=12, fontweight='bold')

# Arrow showing the uplift
ax.annotate(
    f"+${opp_df['extra_monthly_revenue']:,.0f}/mo",
    xy=(1, potential_rev * 0.95),
    xytext=(0.5, potential_rev * 0.75),
    arrowprops=dict(arrowstyle='->', color=TEAL, lw=2),
    color=TEAL, fontsize=12, fontweight='bold',
)

ax.set_ylabel('Monthly Revenue ($)')
ax.set_title('Revenue Opportunity: Fix Mobile Onboarding\n3.6 percentage point conversion gap', fontsize=13, pad=12)
ax.set_ylim(0, potential_rev * 1.2)

plt.tight_layout()
plt.savefig('charts/06_revenue_opportunity.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: charts/06_revenue_opportunity.png")

# ==============================================================
# Summary
# ==============================================================
chart_files = sorted([f for f in os.listdir('charts') if f.endswith('.png')])
print()
print("=" * 55)
print("PHASE 5 COMPLETE — all charts saved")
print("=" * 55)
for f in chart_files:
    print(f"  charts/{f}")
print("=" * 55)
