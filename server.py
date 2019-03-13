from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = '4a136bc896d8e3657d1799320bb2aa37'


@app.route('/')
def survey():
    session['title'] = 'Dojo Survey'
    db = connectToMySQL('dojo_survey')
    query1 = 'SELECT * FROM location'
    query2 = 'SELECT * FROM languages'
    locations = db.query_db(query1)
    db = connectToMySQL('dojo_survey')
    languages = db.query_db(query2)
    print(locations)
    print(languages)
    return render_template('survey.html', locations=locations, languages=languages)



if __name__ == "__main__":
    app.run(debug=True)
