from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = '4a136bc896d8e3657d1799320bb2aa37'


@app.route('/')
def survey():
    return render_template('survey.html')



if __name__ == "__main__":
    app.run(debug=True)
