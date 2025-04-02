from flask import Blueprint, render_template, request, redirect, url_for, session
import bcrypt
import time

main = Blueprint('main', __name__)

# Hardcoded user for now
USERS = {
    "cyberking": bcrypt.hashpw("DarkP@ssw0rd".encode(), bcrypt.gensalt())
}

FAILED_LOGINS = {}

@main.route("/", methods=["GET", "POST"])
def login():
    client_ip = request.remote_addr

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Anti bruteforce : pause en cas d’échec
        attempts = FAILED_LOGINS.get(client_ip, 0)

        # Limite après X tentatives
        if attempts >= 5:
            time.sleep(5)

        hashed = USERS.get(username)
        if hashed and bcrypt.checkpw(password.encode(), hashed):
            session["user"] = username
            FAILED_LOGINS.pop(client_ip, None)  # reset
            return redirect(url_for("main.flag"))

        FAILED_LOGINS[client_ip] = attempts + 1
        time.sleep(1)  # petit délai à chaque fail
        return render_template("login.html", error="Identifiants invalides.")

    return render_template("login.html")


@main.route("/flag")
def flag():
    if session.get("user") != "cyberking":
        return redirect(url_for("main.login"))

    return render_template("flag.html", flag="flag{brute_force_gg}")
