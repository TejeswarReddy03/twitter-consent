from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key

# OAuth Setup
oauth = OAuth(app)
twitter = oauth.register(
    name="twitter",
    client_id="eXSmfJmpJSRifmGxnHI7600RF",  # Replace with your API key
    client_secret="RXzEWKcZ4zUZORoFqBLqvXkvmH2g50Uwk7XdzPWCEPe1sci3eN",  # Replace with your API secret
    request_token_url="https://api.twitter.com/oauth/request_token",
    access_token_url="https://api.twitter.com/oauth/access_token",
    authorize_url="https://api.twitter.com/oauth/authorize",
)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return twitter.authorize_redirect(url_for("callback", _external=True))

@app.route("/callback")
def callback():
    token = twitter.authorize_access_token()
    session["token"] = token
    user_info = token.get("screen_name", "Unknown User")
    session["user"] = user_info
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    user = session.get("user", "Guest")
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
