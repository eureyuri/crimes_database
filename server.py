"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
# accessible as a variable in index.html:
from sqlalchemy import *
from flask import Flask, request, render_template, g, redirect, Response
from dotenv import load_dotenv
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
load_dotenv()

DATABASEURI = os.getenv("DATABASEURI")

# Creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.
    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    if request.method == 'POST':
        location = request.form['location']
        return redirect('/' + location)


@app.route('/<location>')
def location_info(location):
    crimes_cursor = g.conn.execute("SELECT COUNT(*) FROM happened_at WHERE state=%s", location)
    (crimes_number,) = crimes_cursor.fetchone()
    crimes_cursor.close()

    police_crime_cursor = g.conn.execute(
        "SELECT COUNT(*) FROM police_crimes_work_at,happened_at WHERE police_crimes_work_at.case_id=happened_at.case_id AND happened_at.state=%s",
        location)
    (police_crime_number,) = police_crime_cursor.fetchone()
    police_crime_cursor.close()

    police_station_cursor = g.conn.execute("SELECT COUNT(*) FROM police_station_located_at WHERE state=%s", location)
    (police_station_number,) = police_station_cursor.fetchone()
    police_station_cursor.close()

    missing_cursor = g.conn.execute("SELECT COUNT(*) FROM last_seen_at WHERE state=%s", location)
    (missing_number,) = missing_cursor.fetchone()
    missing_cursor.close()

    fugitives_cursor = g.conn.execute("SELECT COUNT(*) FROM recently_seen_at WHERE state=%s", location)
    (fugitives_number,) = fugitives_cursor.fetchone()
    fugitives_cursor.close()

    homicide_cursor = g.conn.execute(
        "SELECT COUNT(*) FROM homicides,happened_at WHERE homicides.case_id=happened_at.case_id AND happened_at.state=%s",
        location)
    (homicide_number,) = homicide_cursor.fetchone()
    homicide_cursor.close()

    context = dict(location=location, number_police_offices=police_station_number, number_crimes=crimes_number,
                   number_police_crimes=police_crime_number, number_homicides=homicide_number,
                   number_missing=missing_number, number_fugitives=fugitives_number)
    return render_template('location.html', **context)


@app.route('/<location>/crimes')
def crimes_info(location):
    data = []
    homicide_crimes_cursor = g.conn.execute(
        "SELECT crimes.case_id,crimes.year,crimes.month, homicides.action_type FROM crimes, homicides, happened_at WHERE crimes.case_id=happened_at.case_id AND crimes.case_id=homicides.case_id AND happened_at.state=%s",
        location)
    for case in homicide_crimes_cursor:
        temp_dict = {'Case ID': case[0], 'year': case[1], 'month': case[2], 'crime_type': case[3]}
        data.append(temp_dict)
    homicide_crimes_cursor.close()
    police_crimes_cursor = g.conn.execute(
        "SELECT crimes.case_id,crimes.year,crimes.month,police_crimes_work_at.crime_type FROM crimes, police_crimes_work_at, happened_at WHERE crimes.case_id=happened_at.case_id AND crimes.case_id=police_crimes_work_at.case_id AND happened_at.state=%s",
        location)
    for case in police_crimes_cursor:
        temp_dict2 = {'Case ID': case[0], 'year': case[1], 'month': case[2], 'crime_type': 'Murder'}
        data.append(temp_dict2)

    police_crimes_cursor.close()
    title = 'Crimes'
    header = ['Case ID', 'Year', 'Month', 'Crime Type']
    context = dict(location=location, title=title, header=header, data=data)
    return render_template('details.html', **context)


@app.route('/<location>/police_offices')
def police_offices_info(location):
    data = []
    police_station_cursor = g.conn.execute(
        "SELECT name,city,address1,zip,tel FROM police_station_located_at WHERE state=%s", location)
    for station in police_station_cursor:
        temp_dict = {'office': station[0], 'city': station[1], 'address1': station[2], 'zip': station[3],
                     'tel': station[4]}
        data.append(temp_dict)

    police_station_cursor.close()

    title = 'Police Offices'
    header = ['Name', 'City', 'Address', 'Zip Code', 'Tel Number']
    context = dict(location=location, title=title, header=header, data=data)
    return render_template('details.html', **context)


@app.route('/<location>/police_crimes')
def police_crimes_info(location):
    data = []
    police_crimes_cursor = g.conn.execute(
        "SELECT police_crimes_work_at.case_id,police_crimes_work_at.arrested_officer_rank,police_crimes_work_at.arrested_officer_age,police_crimes_work_at.arrested_officer_race,police_crimes_work_at.arrested_officer_sex,police_crime_victims.age, police_crime_victims.race,police_crime_victims.sex,police_crime_victims.relation FROM police_crimes_work_at,happened_at,police_crime_victims WHERE police_crime_victims.case_id = police_crimes_work_at.case_id AND police_crimes_work_at.case_id=happened_at.case_id AND happened_at.state=%s",
        location)
    for case in police_crimes_cursor:
        temp_dict = {'case_id': case[0], 'police rank': case[1], 'police age': case[2], 'police race': case[3],
                     'police sex': case[4], 'victim age': case[5], 'victim race': case[6], 'victim sex': case[7],
                     'relation': case[8]}
        data.append(temp_dict)
    police_crimes_cursor.close()

    title = "Police Criminals Information"
    header = ['Case ID', 'PoliceRank', 'PoliceAge', 'PoliceRace', 'PoliceSex', 'VictimAge', 'VictimRace', 'VictimSex',
              'Relation']
    context = dict(location=location, title=title, header=header, data=data)
    return render_template('details.html', **context)


@app.route('/<location>/homicides')
def homicides_info(location):
    data = []
    homicides_cursor = g.conn.execute(
        "SELECT homicides.case_id,homicides.age,homicides.race,homicides.sex,kill_homicide.age, kill_homicide.race,kill_homicide.sex,kill_homicide.relation FROM homicides,happened_at,kill_homicide WHERE kill_homicide.case_id = homicides.case_id AND homicides.case_id=happened_at.case_id AND happened_at.state=%s",
        location)
    for case in homicides_cursor:
        temp_dict = {'case_id': case[0], 'homicide age': case[1], 'homicide race': case[2], 'homicide sex': case[3],
                     'victim age': case[4], 'victim race': case[5], 'victim sex': case[6], 'relation': case[7]}
        data.append(temp_dict)
    homicides_cursor.close()

    title = "Homicides Information"
    header = ['Case ID', 'HomicideAge', 'HomicideRace', 'HomicideSex', 'VictimAge', 'VictimRace', 'VictimSex',
              'Relation']
    context = dict(location=location, title=title, header=header, data=data)
    return render_template('details.html', **context)


@app.route('/<location>/missing')
def missing_info(location):
    data = []
    missing_cursor = g.conn.execute(
        "SELECT missing_people.id,missing_people.name,missing_people.age,missing_people.sex,missing_people.race,missing_people.hair,missing_people.eyes,missing_people.nationality FROM missing_people, last_seen_at WHERE missing_people.id=last_seen_at.id AND last_seen_at.state=%s",
        location)
    for case in missing_cursor:
        temp_dict = {'id': case[0], 'name': case[1], 'age': case[2], 'sex': case[3], 'race': case[4], 'hair': case[5],
                     'eyes': case[6], 'nationality': case[7]}
        data.append(temp_dict)
    missing_cursor.close()
    title = "Missing People Information"
    header = ['Case ID', 'Name', 'Age', 'Sex', 'Race', 'Hair', 'Eyes', 'Nationality']
    context = dict(location=location, title=title, header=header, data=data)
    return render_template('details.html', **context)


@app.route('/<location>/fugitives')
def fugitives_info(location):
    data = []
    fugitives_cursor = g.conn.execute(
        "SELECT fugitives.id,fugitives.name,fugitives.age,fugitives.sex,fugitives.race,fugitives.hair,fugitives.eyes,fugitives.nationality FROM fugitives, recently_seen_at WHERE fugitives.id=recently_seen_at.id AND recently_seen_at.state=%s",
        location)
    for case in fugitives_cursor:
        temp_dict = {'id': case[0], 'name': case[1], 'age': case[2], 'sex': case[3], 'race': case[4], 'hair': case[5],
                     'eyes': case
                     [6], 'nationality': case[7]}
        data.append(temp_dict)
    fugitives_cursor.close()
    title = "Fugitives Information"
    header = ['Case ID', 'Name', 'Age', 'Sex', 'Race', 'Hair', 'Eyes', 'Nationality']
    context = dict(location=location, title=title, header=header, data=data)
    return render_template('details.html', **context)


if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:
            python server.py
        Show the help text using:
            python server.py --help
        """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()