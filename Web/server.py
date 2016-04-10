#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

To run locally in debug mode:

    python server.py --debug

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from datetime import datetime
from flask import Flask
from flask import g
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from sqlalchemy import *
from sqlalchemy.pool import NullPool

from DBUtil import get_first_result
from DBUtil import get_results
from DBUtil import USER_OWN_EVENTS_SQL, USER_JOIN_EVENTS_SQL
from WebUtil import set_cookie_redirct

app = Flask(__name__)


DATABASEURI = "postgresql://hl2907:481516losT_@w4111vm.eastus.cloudapp.azure.com/w4111"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


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
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
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

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

@app.route('/')
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

    # DEBUG: this is debugging code to see what request looks like
    print request.args

    #
    # example of a database query
    #
    # cursor = g.conn.execute("SELECT Name FROM Person")
    # names = []
    # for result in cursor:
    #     names.append(result['name'])  # can also be accessed using result[0]
    # cursor.close()

    #
    # Flask uses Jinja templates, which is an extension to HTML where you can
    # pass data to a template and dynamically generate HTML based on the data
    # (you can think of it as simple PHP)
    # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
    #
    # You can see an example template in templates/index.html
    #
    # context are the variables that are passed to the template.
    # for example, "data" key in the context variable defined below will be 
    # accessible as a variable in index.html:
    #
    #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
    #     <div>{{data}}</div>
    #     
    #     # creates a <div> tag for each element in data
    #     # will print: 
    #     #
    #     #   <div>grace hopper</div>
    #     #   <div>alan turing</div>
    #     #   <div>ada lovelace</div>
    #     #
    #     {% for n in data %}
    #     <div>{{n}}</div>
    #     {% endfor %}
    #
    # context = dict(data = names)


    context = dict()
    username = request.cookies.get('username')
    if username:
        print "there is a username cookie!"
        context = dict(username = username)
    else:
        print "there is no username cookie :("
    # return render_template("index.html", **context)
    return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/test')
def test():
    return render_template("test_semantic.html")

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
    return redirect('/')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form["email"]
        username = request.form["username"]
        cursor = g.conn.execute('SELECT Person_id, Name, Email'                \
                                'FROM Person WHERE Name = %s and Email = %s',  \
                                (username, email))
        result = get_first_result(cursor)
        if result:
            resp = make_response(redirect("/"))
            resp.set_cookie('username', username)
            resp.set_cookie('email', email)
            resp.set_cookie('user_id', str(result[0]))
            return resp
        else:
            # TODO(Chris): Handle the not found case error message
            print "No such user!"
            return render_template("sign_up.html")
        
@app.route('/sign_up', methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("sign_up.html")
    else: # POST
        params = (request.form["username"], request.form["email"],             \
                    request.form["age"], request.form["gender"])
        cursor = g.conn.execute("INSERT INTO Person (Name, Email, Age, Gender)"\
                                "VALUES (%s, %s, %s, %s);", params)
        if cursor:
            # TODO(Chris): Add the user sign up info into cookie like login
            return set_cookie_redirct('username', params[0], "/")
        else:
            # TODO(Chris): Handle the error format for signup, 
            # ex. enter age with not numbers or some db callback
            print "Something happens in DB"
            return render_template("sign_up.html")
        
@app.route('/restaurant')
def restaurant():
    return render_template("restaurant.html")

def collect_events(events):
    return [{'name': event[1],                                                 \
             'desc': event[2],                                                 \
             'time': datetime.combine(event[3], event[4])                      \
                                .strftime("%Y-%m-%d %H:%M:%S"),                \
             'number': event[5]}                                               \
             for event in events]

@app.route('/event')
def event():
    user_id = request.cookies.get("user_id")
    own_cursor = g.conn.execute(USER_OWN_EVENTS_SQL, 99)
    join_cursor = g.conn.execute(USER_JOIN_EVENTS_SQL, 3)
    own_events = get_results(own_cursor)
    join_events = get_results(join_cursor)
    data = dict(own_events=collect_events(own_events),                         \
                join_events=collect_events(join_events))
    return render_template("event.html", **data)

@app.route('/create_event')
def create_event():
    return render_template("create_event.html", **data)

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
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
