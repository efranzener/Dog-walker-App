from http import server
from flask import (Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "Mys3cr3tk3y"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

