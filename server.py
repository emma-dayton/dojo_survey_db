from flask import Flask, render_template, request, redirect, session, flash
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
    is_valid = True
    name = request.form['name']
    if len(name) > 255 or len(name) < 1: # checking that name is a valid length
        is_valid = False
        flash("Please enter a name that is between 1 and 255 characters long")
    dojo = request.form['dojo'] # pull down menu means only valid options available
    lang = request.form['language'] # pull down menu means only valid options available
    comment = request.form['comment']
    if len(comment) > 120: # comments can be empty
        is_valid = False
        flash("Please make sure your comment is at most 120 characters long")
    if not is_valid:
        return redirect ('/')
    data = {'name':name, 'dojo':dojo, 'lang':lang, 'comment':comment}
    session['data'] = data
    return render_template('results.html', data=data)

@app.route('/submit')
def submit():
    print(checkbox, '&&&&&&&&&&&&&***************&&&&&&&&&&&')
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
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
