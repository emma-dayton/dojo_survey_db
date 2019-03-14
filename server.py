from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = '4a136bc896d8e3657d1799320bb2aa37'


@app.route('/')
def survey():
    if 'data' in session:
        session.pop('data')
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

@app.route('/results', methods=['POST'])
def survey_says():
    session['title'] = 'Survey Says...'
    name = request.form['name']
    dojo = request.form['dojo']
    lang = request.form['language']
    comment = request.form['comment']
    data = {'name':name, 'dojo':dojo, 'lang':lang, 'comment':comment}
    session['data'] = data
    return render_template('results.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    db = connectToMySQL('dojo_survey')
    query = "SELECT id FROM location WHERE city = %(city)s;"
    city = session['data']['dojo'].split(',')
    city = {'city':city[0]}
    loc_id = db.query_db(query, city)
    loc_id = loc_id[0]['id']
    db = connectToMySQL('dojo_survey')
    language = session['data']['lang']
    lang = {'lang':language}
    query = "SELECT id FROM languages WHERE lang_name = %(lang)s;"
    lang_id = db.query_db(query, lang)
    print(lang_id, '++++++++++++++++')
    lang_id = lang_id[0]['id']
    db = connectToMySQL('dojo_survey')
    data = {
    'comment':session['data']['comment'],
    'name':session['data']['name'],
    'loc_id':loc_id,
    'lang_id':lang_id
    }
    query = """INSERT INTO users (name, comment, location_id, languages_id)
    VALUES (%(name)s, %(comment)s, %(loc_id)s, %(lang_id)s)"""
    huh = db.query_db(query, data)
    print(huh, '+++++++++++++++++++++++++++++++++')
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
