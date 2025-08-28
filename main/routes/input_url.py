from flask import Blueprint, render_template, request, url_for, redirect
from urllib.parse import urlparse
from src.amazon_scraper import scrape_amazon
import json, os
import asyncio
from playwright.async_api import async_playwright

input_url_bp = Blueprint("input_url", __name__)
secret_key = "mysecret"

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@input_url_bp.route("/input_url", methods = ["GET", "POST"])
def input_url():
    if request.method == "POST":
        url = request.form.get("url")
        if not is_valid_url(url):
            error = "Please enter a valid URL."
            return render_template("input_url.html", error=error)
        
         # scrape reviews
        data = asyncio.run(scrape_amazon(url))

        # create absolute path to static/reviews.json
        json_path = os.path.join(input_url_bp.root_path, "..", "static", "reviews.json")
        json_path = os.path.abspath(json_path)

        # ensure the folder exists
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return redirect(url_for("dashboard.dashboard"))

    return render_template("input_url.html")