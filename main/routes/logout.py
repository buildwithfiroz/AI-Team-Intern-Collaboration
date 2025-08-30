from flask import Blueprint, redirect, url_for, session, flash

logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))
