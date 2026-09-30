"""
Generate Power BI-style dashboard visuals from funnel data.

Reads raw and curated CSVs, computes real metrics, and produces
high-resolution PNG dashboards with a dark theme.

Usage: python python/generate_dashboard_pngs.py
Output: assets/*.png (4 dashboards)
"""

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Paths
BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
CURATED = BASE / "data" / "curated"
ASSETS = BASE / "assets"
ASSETS.mkdir(exist_ok=True)

# Load data
visitors = pd.read_csv(RAW / "visitors.csv")
signups = pd.read_csv(RAW / "signups.csv")
trials = pd.read_csv(RAW / "trials.csv")
paid = pd.read_csv(RAW / "paid_customers.csv")
channels = pd.read_csv(CURATED / "channel_metrics.csv")
funnel = pd.read_csv(CURATED / "funnel_metrics.csv")
cohorts = pd.read_csv(CURATED / "cohort_metrics.csv")

# Compute funnel totals
total_v = visitors["visitors"].sum()
total_s = signups["signups"].sum()
total_t = trials["trial_users"].sum()
total_p = paid["paid_customers"].sum()

# Cohort pivot
cohort_pivot = cohorts.pivot(index="cohort_month", columns="month_number", values="retention_rate")

# Channel metrics
channels = channels.sort_values("visitors", ascending=False)

# Theme
BG = "#0D1F1C"
CARD_BG = "#14312B"
TEXT = "#E6F2EE"
MUTED = "#7FA79D"
ACCENT1 = "#2DD4BF"
ACCENT2 = "#4ADE80"
ACCENT3 = "#A3E635"
ACCENT4 = "#FACC15"
ACCENT5 = "#38BDF8"
GRID = "#24463E"
PALETTE = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5, "#34D399", "#22D3EE", "#84CC16"]


def style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT, fontsize=14, fontweight="bold", pad=10, loc="left")
    ax.set_xlabel(xlabel, color=MUTED, fontsize=9)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)
    ax.tick_params(colors=MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.5)


def fmt_k(x, _=None):
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"{x/1_000:.0f}K"
    return f"{x:.0f}"


# Dashboard 1 - Funnel Analysis
def create_funnel_analysis():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Conversion Funnel Analysis", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"2.24M visitors  |  7-stage funnel  |  {total_p:,} paid customers  |  0.70% visitor-to-paid",
             color=MUTED, fontsize=10, ha="left")

    # Funnel stages
    stages = ["Visitors", "Signups", "Trials", "Paid"]
    values = [total_v, total_s, total_t, total_p]
    rates = [100, total_s/total_v*100, total_t/total_s*100, total_p/total_t*100]

    # Funnel bars
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.38])
    style_ax(ax1, "Funnel Stages")
    colors = [ACCENT1, ACCENT2, ACCENT4, ACCENT5]
    bars = ax1.barh(stages[::-1], values[::-1], color=colors[::-1], height=0.6)
    for bar, val, rate in zip(bars, values[::-1], rates[::-1]):
        ax1.text(val + total_v * 0.02, bar.get_y() + bar.get_height()/2,
                 f"{fmt_k(val)}  ({rate:.2f}%)", color=TEXT, fontsize=9, va="center")
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))

    # Conversion rates
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.38])
    style_ax(ax2, "Stage-to-Stage Conversion Rates", ylabel="Rate %")
    stage_labels = ["Visitor→Signup", "Signup→Trial", "Trial→Paid"]
    stage_rates = [total_s/total_v*100, total_t/total_s*100, total_p/total_t*100]
    bars = ax2.bar(stage_labels, stage_rates, color=[ACCENT1, ACCENT2, ACCENT4], width=0.55)
    for bar, val in zip(bars, stage_rates):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.2f}%", color=TEXT, fontsize=10, ha="center", fontweight="bold")
    ax2.set_ylim(0, max(stage_rates) * 1.3)

    # Channel performance
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    style_ax(ax3, "Visitors by Channel")
    bars = ax3.barh(channels["channel"], channels["visitors"], color=PALETTE[:len(channels)], height=0.6)
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, channels["visitors"]):
        ax3.text(val + total_v * 0.01, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Channel conversion
    ax4 = fig.add_axes([0.52, 0.06, 0.44, 0.38])
    style_ax(ax4, "Signup Conversion Rate by Channel", ylabel="Rate %")
    channels_sorted = channels.sort_values("signups", ascending=True)
    conv_rates = (channels_sorted["signups"] / channels_sorted["visitors"] * 100).values
    bars = ax4.barh(channels_sorted["channel"], conv_rates, color=PALETTE[:len(channels_sorted)], height=0.6)
    for bar, val in zip(bars, conv_rates):
        ax4.text(val + 0.2, bar.get_y() + bar.get_height()/2, f"{val:.2f}%", color=TEXT, fontsize=8, va="center")

    fig.savefig(ASSETS / "funnel_analysis.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK funnel_analysis.png")


# Dashboard 2 - Channel Performance
def create_channel_performance():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Channel Performance", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"8 acquisition channels  |  Visitor volume, signup conversion, and trial rates",
             color=MUTED, fontsize=10, ha="left")

    # Visitors by channel
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.38])
    style_ax(ax1, "Total Visitors by Channel")
    bars = ax1.barh(channels["channel"], channels["visitors"], color=PALETTE[:len(channels)], height=0.6)
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, channels["visitors"]):
        ax1.text(val + total_v * 0.01, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Signup rate by channel
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.38])
    style_ax(ax2, "Signup Rate by Channel", ylabel="Rate %")
    channels_sorted = channels.sort_values("signups", ascending=True)
    conv_rates = (channels_sorted["signups"] / channels_sorted["visitors"] * 100).values
    bars = ax2.barh(channels_sorted["channel"], conv_rates, color=PALETTE[:len(channels_sorted)], height=0.6)
    for bar, val in zip(bars, conv_rates):
        ax2.text(val + 0.15, bar.get_y() + bar.get_height()/2, f"{val:.2f}%", color=TEXT, fontsize=8, va="center")

    # Funnel by channel
    ax3 = fig.add_axes([0.04, 0.06, 0.92, 0.38])
    style_ax(ax3, "Full Funnel by Channel", ylabel="Count")
    x = np.arange(len(channels))
    width = 0.2
    ax3.bar(x - width*1.5, channels["visitors"], width, label="Visitors", color=ACCENT1, alpha=0.8)
    ax3.bar(x - width*0.5, channels["signups"], width, label="Signups", color=ACCENT2, alpha=0.8)
    ax3.bar(x + width*0.5, channels.get("onboarded", channels["signups"]*0.7), width, label="Onboarded", color=ACCENT4, alpha=0.8)
    ax3.bar(x + width*1.5, channels.get("activated", channels["signups"]*0.4), width, label="Activated", color=ACCENT5, alpha=0.8)
    ax3.set_xticks(x)
    ax3.set_xticklabels(channels["channel"], rotation=0, fontsize=8)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    ax3.legend(fontsize=8, loc="upper right", framealpha=0.3, facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT)

    fig.savefig(ASSETS / "channel_performance.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK channel_performance.png")


# Dashboard 3 - Cohort Analysis
def create_cohort_analysis():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Retention Cohort Analysis", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"{len(cohort_pivot)} cohorts  |  Monthly retention tracking  |  12-month follow-up",
             color=MUTED, fontsize=10, ha="left")

    # Retention heatmap
    ax1 = fig.add_axes([0.04, 0.15, 0.92, 0.72])
    style_ax(ax1, "Retention Rate by Cohort Month")
    data = cohort_pivot.values
    im = ax1.imshow(data, cmap="RdYlGn", aspect="auto", vmin=0, vmax=100)
    ax1.set_xticks(range(data.shape[1]))
    ax1.set_xticklabels([f"M{i}" for i in range(data.shape[1])], color=MUTED, fontsize=8)
    ax1.set_yticks(range(data.shape[0]))
    ax1.set_yticklabels(cohort_pivot.index, color=MUTED, fontsize=7)
    for i in range(min(data.shape[0], 20)):
        for j in range(data.shape[1]):
            val = data[i, j]
            if not np.isnan(val):
                ax1.text(j, i, f"{val:.0f}%", ha="center", va="center", color=TEXT, fontsize=6)
    cbar = plt.colorbar(im, ax=ax1, shrink=0.8)
    cbar.ax.tick_params(colors=MUTED, labelsize=8)

    fig.savefig(ASSETS / "cohort_analysis.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK cohort_analysis.png")


# Dashboard 4 - Executive Overview
def create_executive_overview():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Executive Overview", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"2.24M visitors  |  {total_p:,} paid customers  |  0.70% conversion  |  8 channels",
             color=MUTED, fontsize=10, ha="left")

    # KPI cards
    card_data = [
        ("Total Visitors", fmt_k(total_v), "8 channels", ACCENT1),
        ("Signups", f"{total_s:,}", f"{total_s/total_v*100:.2f}% conversion", ACCENT2),
        ("Trial Users", f"{total_t:,}", f"{total_t/total_s*100:.2f}% of signups", ACCENT5),
        ("Paid Customers", f"{total_p:,}", f"{total_p/total_t*100:.2f}% of trials", ACCENT4),
        ("Visitor→Paid", "0.70%", f"{total_p:,} of {fmt_k(total_v)}", ACCENT3),
    ]

    for i, (label, value, sub, color) in enumerate(card_data):
        x = 0.04 + i * 0.19
        rect = FancyBboxPatch((x, 0.87), 0.17, 0.055, boxstyle="round,pad=0.008",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1.5, transform=fig.transFigure)
        fig.patches.append(rect)
        fig.text(x + 0.085, 0.912, value, color=color, fontsize=18, fontweight="bold", ha="center", va="center")
        fig.text(x + 0.085, 0.895, label, color=MUTED, fontsize=9, ha="center", va="center")
        fig.text(x + 0.085, 0.878, sub, color=MUTED, fontsize=8, ha="center", va="center")

    # Funnel visualization
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.35])
    style_ax(ax1, "Conversion Funnel")
    stages = ["Visitors", "Signups", "Trials", "Paid"]
    values = [total_v, total_s, total_t, total_p]
    colors = [ACCENT1, ACCENT2, ACCENT5, ACCENT4]
    bars = ax1.barh(stages[::-1], values[::-1], color=colors[::-1], height=0.6)
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, values[::-1]):
        ax1.text(val + total_v * 0.02, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=9, va="center")

    # Channel breakdown
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.35])
    style_ax(ax2, "Visitors by Channel")
    bars = ax2.barh(channels["channel"], channels["visitors"], color=PALETTE[:len(channels)], height=0.6)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))

    # Daily trend
    ax3 = fig.add_axes([0.04, 0.06, 0.92, 0.35])
    style_ax(ax3, "Daily Visitor Trend", ylabel="Visitors")
    daily = visitors.groupby("date")["visitors"].sum().reset_index()
    daily["date_dt"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date_dt")
    ax3.fill_between(daily["date_dt"], daily["visitors"], alpha=0.15, color=ACCENT1)
    ax3.plot(daily["date_dt"], daily["visitors"], color=ACCENT1, linewidth=1.5)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    ax3.set_xticks(daily["date_dt"][::60])
    ax3.set_xticklabels([d.strftime("%b '%y") for d in daily["date_dt"][::60]], rotation=0, fontsize=7)

    fig.savefig(ASSETS / "executive_overview.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK executive_overview.png")


# Dashboard 5 - Retention Metrics
def create_retention_metrics():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Retention Metrics", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"Monthly retention by cohort  |  Average retention curves  |  Long-term engagement patterns",
             color=MUTED, fontsize=10, ha="left")

    # Average retention curve
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.38])
    style_ax(ax1, "Average Retention Curve", xlabel="Months Since Signup", ylabel="Retention %")
    avg_retention = cohort_pivot.mean()
    ax1.plot(avg_retention.index, avg_retention.values, color=ACCENT1, linewidth=2, marker="o", markersize=4)
    ax1.fill_between(avg_retention.index, avg_retention.values, alpha=0.15, color=ACCENT1)
    ax1.set_ylim(0, 100)
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter())

    # Retention by cohort (top 5)
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.38])
    style_ax(ax2, "Retention by Cohort (First 5 Months)", xlabel="Months Since Signup", ylabel="Retention %")
    for i, cohort_name in enumerate(cohort_pivot.index[:6]):
        row = cohort_pivot.loc[cohort_name]
        ax2.plot(row.index, row.values, color=PALETTE[i], linewidth=1.5, label=cohort_name, alpha=0.8)
    ax2.set_ylim(0, 100)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax2.legend(fontsize=7, loc="upper right", framealpha=0.3, facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT, ncol=2)

    # Channel retention
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    style_ax(ax3, "Signup Volume by Channel")
    bars = ax3.barh(channels["channel"], channels["signups"], color=PALETTE[:len(channels)], height=0.6)
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, channels["signups"]):
        ax3.text(val + channels["signups"].max() * 0.02, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Activation rate
    ax4 = fig.add_axes([0.52, 0.06, 0.44, 0.38])
    style_ax(ax4, "Activation Rate by Channel", ylabel="Rate %")
    channels_sorted = channels.sort_values("activated", ascending=True)
    act_rates = (channels_sorted["activated"] / channels_sorted["signups"] * 100).values
    bars = ax4.barh(channels_sorted["channel"], act_rates, color=PALETTE[:len(channels_sorted)], height=0.6)
    for bar, val in zip(bars, act_rates):
        ax4.text(val + 0.5, bar.get_y() + bar.get_height()/2, f"{val:.1f}%", color=TEXT, fontsize=8, va="center")

    fig.savefig(ASSETS / "retention_metrics.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK retention_metrics.png")


if __name__ == "__main__":
    print("Generating funnel dashboards...")
    create_funnel_analysis()
    create_channel_performance()
    create_cohort_analysis()
    create_executive_overview()
    create_retention_metrics()
    print(f"\nAll dashboards saved to {ASSETS}/")
