from flask import Blueprint, render_template
from database.connection import get_db_connection
from datetime import datetime
from collections import Counter

dashboard_bp = Blueprint("dashboard", __name__)

def clean_rating(raw_rating):
    """
    Rating ko string se float me convert karega.
    Example: "4.0 out of 5 stars" -> 4.0
    """
    try:
        if raw_rating is None:
            return 0.0
        # Agar string hai to split karega
        rating_str = str(raw_rating).strip()
        if rating_str == "":
            return 0.0
        return float(rating_str.split()[0])  # sirf pehla number lega
    except Exception:
        return 0.0


@dashboard_bp.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Products
    cursor.execute("SELECT image FROM product")
    products = cursor.fetchall()
    products = [{"image": row[0]} for row in products]

    # ✅ Latest 10 Reviews
    cursor.execute("""
        SELECT name, rating, title, date, body
        FROM reviews
        ORDER BY date DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    reviews = [
        {
            "name": row[0],
            "rating": int(round(clean_rating(row[1]))),  # ensure integer for stars
            "title": row[2],
            "date": row[3],
            "body": row[4]
        }
        for row in rows
    ]

    # ✅ Top 5 Reviews
    cursor.execute("""
        SELECT name, rating, title, date, body
        FROM reviews
        ORDER BY CAST(SUBSTR(rating, 1, 3) AS FLOAT) DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    top_reviews = [
        {
            "name": row[0],
            "rating": int(round(clean_rating(row[1]))),
            "title": row[2],
            "date": row[3],
            "body": row[4]
        }
        for row in rows
    ]

    # ✅ Total Reviews
    cursor.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cursor.fetchone()[0]

    # ✅ Avg Rating
    cursor.execute("SELECT rating FROM reviews")
    all_ratings = [clean_rating(r[0]) for r in cursor.fetchall()]
    avg_rating = round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else 0

    # ✅ Dummy values
    response_rate = 92
    recent_orders = 15

    # ✅ Line Chart Data
    cursor.execute("SELECT date FROM reviews")
    all_dates = [row[0] for row in cursor.fetchall()]
    conn.close()

    cleaned_months = []
    for raw_date in all_dates:
        try:
            if raw_date and "on " in raw_date:
                date_part = raw_date.split("on ")[1]
                dt = datetime.strptime(date_part, "%d %B %Y")
                month_str = dt.strftime("%Y-%m")
                cleaned_months.append(month_str)
        except Exception as e:
            print("Skipping invalid date:", raw_date, e)

    counts_dict = Counter(cleaned_months)
    months = sorted(counts_dict.keys())
    counts = [counts_dict[m] for m in months]

    return render_template(
        "dashboard.html",
        products=products,
        reviews=reviews,
        top_reviews=top_reviews,
        months=months,
        counts=counts,
        total_reviews=total_reviews,
        avg_rating=avg_rating,
        response_rate=response_rate,
        recent_orders=recent_orders
    )
