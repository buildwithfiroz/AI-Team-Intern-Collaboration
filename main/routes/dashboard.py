from flask import Blueprint, render_template
from collections import Counter
from datetime import datetime
import json, os

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():

    json_path = os.path.join("main", "static", "reviews.json")
    reviews = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            reviews = data.get("reviews", [])
            product = data.get("product", {})
    else:
        reviews = []
        product = {}

    # bar chart
    bar_chart_review = reviews
    star_counts = Counter([int(float(r['rating'])) for r in bar_chart_review])
    star_data = [star_counts.get(i, 0) for i in range(1, 6)]

    # line chart
    # --- Line Chart (Reviews per Date) ---
    date_counts = Counter()
    for r in reviews:
        raw_date = r.get("date", "").replace("Reviewed in India on ", "").strip()
        try:
            parsed = datetime.strptime(raw_date, "%d %B %Y")
            formatted = parsed.strftime("%b %Y") 
            date_counts[formatted] += 1
        except ValueError:
            continue

    # Sort by date
    sorted_dates = sorted(date_counts.keys(), key=lambda d: datetime.strptime(d, "%b %Y"))
    line_labels = sorted_dates
    line_data = [date_counts[d] for d in sorted_dates]


    return render_template("dashboard.html", product=product, reviews=reviews, star_data=star_data, line_labels=line_labels, line_data=line_data)