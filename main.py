from flask import Flask
from flask import request, render_template,redirect,url_for

app = Flask(__name__)

@app.route('/')
def index():
    return "method used: %s" % request.method

@app.route("/p/<name>", methods=['GET','POST'])
def profile(name):
    return render_template("profile.html", name=name)

@app.route("/add_user", methods=['GET','POST'])
def add_user_func():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)