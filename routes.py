# Importing the Flask Framework

from modules import *
from flask import *
import database
import configparser


page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
unikey = config['DATABASE']['user']
portchoice = config['FLASK']['port']

#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['unikey'] = unikey
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

################################################################################
# Login Page
################################################################################

# This is for the login
# Look at the methods [post, get] that corresponds with form actions etc.
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'unikey' : unikey}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['sid'], request.form['password'])

        # If our database connection gave back an error
        if(val == None):
            flash("""Error with the database connection. Please check your terminal
            and make sure you updated your INI files.""")
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        session['name'] = val[1]
        session['sid'] = request.form['sid']
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)


################################################################################
# Logout Endpoint
################################################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))


################################################################################
# Transcript Page
################################################################################

@app.route('/transcript')
def transcript():
    # TODO
    # Now it's your turn to add to this ;)
    # Good luck!
    #   Look at the function below
    #   Look at database.py
    #   Look at units.html and transcript.html
    return render_template('transcript.html', page=page, session=session)


################################################################################
# List Units page
################################################################################

# List the units of study
@app.route('/list-units')
def list_units():
    # Go into the database file and get the list_units() function
    units = database.list_units()

    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Units of Study'
    return render_template('units.html', page=page, session=session, units=units)

@app.route('/list-lectures')
def list_lectures():
    lectures = database.list_lectures()
    if (lectures is None):
        # Set it to an empty list and show error message
        lectures = []
        flash('Error, there is no result')
    page['title'] = 'Lectures Info'
    return render_template('lectures.html', page=page, session=session, lectures=lectures)

@app.route('/search-lecture', methods =["GET", "POST"])
def search_lecture():
    searchs = []
    if request.method == "POST":
        time = request.form.get("time")
        searchs = database.search_lecture(time)
        if (searchs is None):
            searchs = []
            flash('Error, there is no result')
    return render_template("search_lecture.html", page=page, session=session, searchs=searchs)

@app.route('/count-classes-classroom')
def count_class_classroom():
    classes = database.count_classes_classroom()
    if (classes is None):
        # Set it to an empty list and show error message
        classes = []
        flash('Error, there is no result')
    page['title'] = 'How many classes are held in every classroom'
    return render_template('count_classes_classroom.html', page=page, session=session, classes=classes)

@app.route('/add-lecture', methods =["GET", "POST"])
def add_lecture():
    adds = []
    if request.method == "POST":
        uoSCode = request.form.get("uoSCode")
        semester = request.form.get("semester")
        year = request.form.get("year")
        classTime = request.form.get("classTime")
        classroomId = request.form.get("classroomId")
        adds = database.add_lecture(uoSCode, semester, year, classTime, classroomId)
        if (adds == False):
            flash('Error, you failed to add because some of your input is illegal.')
        else:
            flash('You Successfully add a new lecture.')
    return render_template("add_lecture.html", page=page, session=session, adds=adds)

# extension
@app.route('/year_count')
def year_count():
    classes = database.year_count()
    if (classes is None):
        # Set it to an empty list and show error message
        classes = []
        flash('Error, there is no result')
    page['title'] = 'How many lectures are held in every classroom'
    return render_template('count_classes_classroom.html', page=page, session=session, classes=classes)

