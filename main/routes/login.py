from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.connection import get_db_connection
import time

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        emailid = request.form.get("emailid")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE emailid = ? AND password = ?",
            (emailid, password)
        ).fetchone()
        conn.close()

        if user:
            session["emailid"] = user["emailid"]
            return redirect(url_for("input_url.input_url"))
        else:
            flash("Invalid Email ID or Password", "error")
            return render_template("login.html")
        
    return render_template("login.html")
