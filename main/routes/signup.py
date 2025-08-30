from flask import Blueprint, render_template, request, flash, redirect, url_for
from database.connection import get_db_connection

signup_bp = Blueprint("signup", __name__)

@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        contactno = request.form.get("contactno")
        emailid = request.form.get("emailid")
        password = request.form.get("password")

        name = f"{firstname} {lastname}"

        # Insert into DB
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (name, contactno, emailid, password) VALUES (?, ?, ?, ?)",
                (name, contactno, emailid, password)
            )
            conn.commit()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("login.login"))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            conn.close()

    return render_template("signup.html")