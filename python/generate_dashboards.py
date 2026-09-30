"""
Generate data-driven Funnel dashboard from actual CSV data.

Reads raw and curated CSVs, computes real metrics, and produces
an interactive HTML dashboard with Chart.js.

Usage: python python/generate_dashboards.py
Output: assets/dashboard.html
"""

import csv
import json
import tempfile
from collections import defaultdict
from pathlib import Path

# Chart.js is inlined when a local copy exists (CI downloads one), so the
# dashboard works offline and without depending on a CDN at view time.
CHART_JS = Path(tempfile.gettempdir()) / "chart.min.js"
CHART_JS_URL = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
if CHART_JS.exists():
    CHART_JS_TAG = "<script>\n" + CHART_JS.read_text(encoding="utf-8") + "\n</script>"
else:
    CHART_JS_TAG = f'<script src="{CHART_JS_URL}"></script>'


ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = ROOT / "assets" / "dashboard.html"


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_metrics():
    visitors = read_csv(DATA_DIR / "raw" / "visitors.csv")
    funnel = read_csv(DATA_DIR / "curated" / "funnel_metrics.csv")

    total_visitors = sum(int(v["visitors"]) for v in visitors)
    total_signups = sum(int(f["signups"]) for f in funnel)
    total_trials = sum(int(f["trial_users"]) for f in funnel)
    total_paid = sum(int(f["paid_customers"]) for f in funnel)
    total_activated = sum(int(f["activated"]) for f in funnel)
    total_mrr = sum(float(f["mrr"]) for f in funnel)

    # Conversion rates
    signup_rate = round(total_signups / total_visitors * 100, 2)
    trial_rate = round(total_trials / total_signups * 100, 2) if total_signups else 0
    paid_rate = round(total_paid / total_trials * 100, 2) if total_trials else 0
    overall_rate = round(total_paid / total_visitors * 100, 3)

    # Channel breakdown
    channel_data = defaultdict(lambda: {"visitors": 0, "signups": 0, "paid": 0, "mrr": 0})
    for f in funnel:
        ch = f["channel"]
        channel_data[ch]["visitors"] += int(f["visitors"])
        channel_data[ch]["signups"] += int(f["signups"])
        channel_data[ch]["paid"] += int(f["paid_customers"])
        channel_data[ch]["mrr"] += float(f["mrr"])

    # Channel conversion rates
    channel_conv = {}
    for ch, d in channel_data.items():
        channel_conv[ch] = round(d["paid"] / d["visitors"] * 100, 2) if d["visitors"] else 0
    channel_conv = dict(sorted(channel_conv.items(), key=lambda x: -x[1]))

    # Monthly trend
    monthly = defaultdict(lambda: {"visitors": 0, "signups": 0, "paid": 0, "mrr": 0})
    for f in funnel:
        m = f["date"][:7]
        monthly[m]["visitors"] += int(f["visitors"])
        monthly[m]["signups"] += int(f["signups"])
        monthly[m]["paid"] += int(f["paid_customers"])
        monthly[m]["mrr"] += float(f["mrr"])
    months_sorted = sorted(monthly.keys())

    # Device breakdown from visitors
    device_data = defaultdict(int)
    for v in visitors:
        device_data[v.get("device", "Unknown")] += int(v["visitors"])

    return {
        "total_visitors": total_visitors,
        "total_signups": total_signups,
        "total_trials": total_trials,
        "total_paid": total_paid,
        "total_activated": total_activated,
        "total_mrr": total_mrr,
        "signup_rate": signup_rate,
        "trial_rate": trial_rate,
        "paid_rate": paid_rate,
        "overall_rate": overall_rate,
        "channels": dict(channel_data),
        "channel_conv": channel_conv,
        "months": months_sorted,
        "monthly_visitors": [monthly[m]["visitors"] for m in months_sorted],
        "monthly_signups": [monthly[m]["signups"] for m in months_sorted],
        "monthly_paid": [monthly[m]["paid"] for m in months_sorted],
        "monthly_mrr": [round(monthly[m]["mrr"] / 1000, 1) for m in months_sorted],
        "devices": dict(sorted(device_data.items(), key=lambda x: -x[1])),
    }


def generate_html(m):
    channels = list(m["channel_conv"].keys())
    conv_rates = list(m["channel_conv"].values())

    # Funnel stages
    stages = [
        ("Visitors", m["total_visitors"], 100),
        ("Signups", m["total_signups"], round(m["total_signups"]/m["total_visitors"]*100,1)),
        ("Activated", m["total_activated"], round(m["total_activated"]/m["total_signups"]*100,1)),
        ("Trial Users", m["total_trials"], round(m["total_trials"]/m["total_activated"]*100,1)),
        ("Paid Customers", m["total_paid"], round(m["total_paid"]/m["total_trials"]*100,1)),
    ]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Conversion Funnel</title>
    {CHART_JS_TAG}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f5f7fa; color: #1e293b; }}
        .topbar {{ background: #1e293b; color: #fff; padding: 10px 24px; display: flex; justify-content: space-between; align-items: center; }}
        .topbar h1 {{ font-size: 15px; font-weight: 600; }}
        .topbar .sub {{ color: #94a3b8; font-size: 11px; }}
        .dash {{ padding: 16px 24px; }}
        .kpi-row {{ display: grid; grid-template-columns: repeat(5,1fr); gap: 14px; margin-bottom: 16px; }}
        .kpi {{ background: #fff; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); border-top: 3px solid #6366f1; }}
        .kpi:nth-child(2) {{ border-top-color: #14b8a6; }}
        .kpi:nth-child(3) {{ border-top-color: #f59e0b; }}
        .kpi:nth-child(4) {{ border-top-color: #ef4444; }}
        .kpi:nth-child(5) {{ border-top-color: #8b5cf6; }}
        .kpi-label {{ font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }}
        .kpi-val {{ font-size: 26px; font-weight: 700; }}
        .kpi-note {{ font-size: 10px; color: #94a3b8; margin-top: 3px; }}
        .row {{ display: grid; gap: 14px; margin-bottom: 16px; }}
        .row-2 {{ grid-template-columns: 3fr 2fr; }}
        .row-eq {{ grid-template-columns: 1fr 1fr; }}
        .box {{ background: #fff; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); }}
        .box-title {{ font-size: 12px; font-weight: 600; color: #475569; margin-bottom: 12px; text-transform: uppercase; }}
        .funnel {{ display: flex; align-items: flex-end; justify-content: center; gap: 2px; margin: 16px 0; }}
        .funnel-stage {{ display: flex; flex-direction: column; align-items: center; }}
        .funnel-bar {{ width: 90px; border-radius: 4px 4px 0 0; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; font-size: 13px; }}
        .funnel-label {{ font-size: 9px; color: #64748b; margin-top: 4px; text-align: center; }}
        .funnel-rate {{ font-size: 9px; color: #94a3b8; margin-bottom: 2px; }}
        .footer {{ text-align: center; padding: 14px; font-size: 10px; color: #cbd5e1; }}
    </style>
</head>
<body>
<div class="topbar">
    <h1>&#x1F4C8; E-Commerce Conversion Funnel</h1>
    <span class="sub">{m['total_visitors']:,} visitors &middot; 5,848 daily-channel records &middot; Generated from live data</span>
</div>
<div class="dash">
    <div class="kpi-row">
        <div class="kpi"><div class="kpi-label">Total Visitors</div><div class="kpi-val">{m['total_visitors']/1e6:.2f}M</div><div class="kpi-note">5,848 day-channel records</div></div>
        <div class="kpi"><div class="kpi-label">Visitor &rarr; Signup</div><div class="kpi-val">{m['signup_rate']}%</div><div class="kpi-note">{m['total_signups']:,} signups</div></div>
        <div class="kpi"><div class="kpi-label">Trial &rarr; Paid</div><div class="kpi-val">{m['paid_rate']}%</div><div class="kpi-note">{m['total_paid']:,} paid customers</div></div>
        <div class="kpi"><div class="kpi-label">Overall Conversion</div><div class="kpi-val">{m['overall_rate']}%</div><div class="kpi-note">Visitor to paid</div></div>
        <div class="kpi"><div class="kpi-label">MRR</div><div class="kpi-val">${m['total_mrr']/1000:.0f}K</div><div class="kpi-note">{m['total_paid']:,} paying customers</div></div>
    </div>

    <div class="box" style="margin-bottom:16px">
        <div class="box-title">Conversion Funnel</div>
        <div class="funnel">
            {"".join(f'''<div class="funnel-stage">
                <div class="funnel-rate">{rate}%</div>
                <div class="funnel-bar" style="height:{max(30, int(count/m["total_visitors"]*300))}px;background:{["#6366f1","#818cf8","#14b8a6","#f59e0b","#ef4444"][i]}">{count:,}</div>
                <div class="funnel-label">{name}</div>
            </div>''' + ('<div style="color:#cbd5e1;font-size:16px;padding-bottom:30px">&rarr;</div>' if i < len(stages)-1 else '') for i, (name, count, rate) in enumerate(stages))}
        </div>
    </div>

    <div class="row row-2">
        <div class="box">
            <div class="box-title">Conversion Rate by Channel</div>
            <canvas id="channelConv" height="190"></canvas>
        </div>
        <div class="box">
            <div class="box-title">Monthly MRR Trend ($K)</div>
            <canvas id="mrrTrend" height="190"></canvas>
        </div>
    </div>

    <div class="row row-eq">
        <div class="box">
            <div class="box-title">Monthly Visitors &amp; Signups</div>
            <canvas id="monthlyTrend" height="190"></canvas>
        </div>
        <div class="box">
            <div class="box-title">Visitors by Device</div>
            <canvas id="deviceBar" height="190"></canvas>
        </div>
    </div>
</div>
<div class="footer">E-Commerce Conversion Funnel &middot; SQL &middot; Python &middot; Power BI &middot; DAX &middot; 7-Stage Funnel</div>

<script>
const months = {json.dumps([mm[-5:] for mm in m['months']])};

new Chart(document.getElementById('channelConv'), {{
    type: 'bar',
    data: {{ labels: {json.dumps(channels)}, datasets: [{{ data: {json.dumps(conv_rates)}, backgroundColor: channels.map((_,i) => `hsl(${{230+i*15}},65%,${{50+i*3}}%)`), borderRadius: 3 }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ ticks: {{ callback: v => v+'%' }}, grid: {{ color: '#f1f5f9' }} }}, x: {{ grid: {{ display: false }} }} }} }}
}});

new Chart(document.getElementById('mrrTrend'), {{
    type: 'line',
    data: {{ labels: months, datasets: [{{ label: 'MRR ($K)', data: {json.dumps(m['monthly_mrr'])}, borderColor: '#8b5cf6', backgroundColor: 'rgba(139,92,246,0.08)', fill: true, tension: 0.3, pointRadius: 3, borderWidth: 2 }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ ticks: {{ callback: v => '$'+v+'K' }}, grid: {{ color: '#f1f5f9' }} }}, x: {{ grid: {{ display: false }} }} }} }}
}});

new Chart(document.getElementById('monthlyTrend'), {{
    type: 'bar',
    data: {{ labels: months, datasets: [
        {{ label: 'Visitors', data: {json.dumps(m['monthly_visitors'])}, backgroundColor: 'rgba(99,102,241,0.6)', borderRadius: 2 }},
        {{ label: 'Signups', data: {json.dumps(m['monthly_signups'])}, backgroundColor: 'rgba(20,184,166,0.6)', borderRadius: 2 }}
    ]}},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10 }} }} }} }}, scales: {{ y: {{ grid: {{ color: '#f1f5f9' }} }}, x: {{ grid: {{ display: false }}, ticks: {{ maxRotation: 45 }} }} }} }}
}});

new Chart(document.getElementById('deviceBar'), {{
    type: 'bar',
    data: {{ labels: {json.dumps(list(m['devices'].keys()))}, datasets: [{{ data: {json.dumps(list(m['devices'].values()))}, backgroundColor: ['#6366f1','#14b8a6','#f59e0b'], borderRadius: 3 }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ grid: {{ color: '#f1f5f9' }} }}, x: {{ grid: {{ display: false }} }} }} }}
}});
</script>
</body>
</html>"""


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    m = compute_metrics()
    html = generate_html(m)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {OUTPUT}")
    print(f"  Visitors: {m['total_visitors']:,} | Signups: {m['total_signups']:,} | Paid: {m['total_paid']:,}")
    print(f"  Signup: {m['signup_rate']}% | Trial: {m['trial_rate']}% | Paid: {m['paid_rate']}% | Overall: {m['overall_rate']}%")


if __name__ == "__main__":
    main()
