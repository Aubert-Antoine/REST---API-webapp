import os
import pathlib
from unicodedata import name

import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Flask REST API auberta")
app.secret_key = "FlaskSpinprojectKey"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "62214700482-1f5bktiq0tnhlpns30r75jq6j0b9jf8i.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):

        # print('\n')
        # for id in session["goole_id"]:
        # print(id)

        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    """
    It is redirection URI for google consol of OAuth
    """
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    print("\n")
    print("\n")
    print(type(session))
    print(session.keys())
    print(type(session["google_id"]))
    print("\n")
    print("\n")

    if(session["google_id"] == "118244919464494232513"):
        return redirect("/protected_area")
    else : 
        return redirect("/OAuth_prb")


@app.route("/OAuth_prb")
def OAuth_prb():
    return render_template("OAuth_prb.html", keys=session.keys(), google_id = session["google_id"], state=session["state"], name=session["name"], type=type(session["google_id"]))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template("protected_area.html", name=session['name'])


##
# CRUD fonction 
##

@app.route("/create")
# @login_is_required
def create():
    return render_template("create.html")


@app.route("/read")
def read():
    return render_template("read.html")

@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/delete")
def delete():
    return render_template("delete.html")


##
# run 
##

if __name__ == "__main__":
    app.run(debug=True)