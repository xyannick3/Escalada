"""
main file to launch our project web page.
"""
from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify

app = Flask(__name__)

app.secret_key = b"thiswebsiteprotectionisnotgreatbecauseitisnotarealone"

@app.route("/")
def home():
    """home page"""
    return render_template("home.html", connected = True, pfp = None)



if __name__ == '__main__':
    app.run(debug = True)
