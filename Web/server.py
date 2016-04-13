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
from flask import url_for
from sqlalchemy import *
from sqlalchemy.pool import NullPool

from DBUtil import get_first_result
from DBUtil import get_results
from DBUtil import DATABASEURI, FIND_USER_OWN_EVENTS_SQL,                      \
                    SIGNUP_USER_SQL, FIND_USER_JOIN_EVENTS_SQL, CREATE_OWN_SQL,\
                    GET_LAST_USER_ID_SQL, LOGIN_USER_SQL,                      \
                    CREATE_EVENT_SQL, FIND_EVENT_WITH_ID_SQL, JOIN_EVENT_SQL,  \
                    FIND_ALL_FEATURES_SQL, FIND_ALL_REGION_ID_ZIPCODE_SQL,     \
                    FIND_RESTAURANT_BY_ZIPCODE, FIND_RESTAURANT_BY_FEATURE,    \
                    FIND_RESTAURANT_BY_ZIPCODE_AND_FEATURE,                    \
                    FIND_RESTAURANT_WITH_REVIEW_BY_ID, ADD_REVIEW_SQL,         \
                    FIND_EVENTS_USER_NOT_IN_SQL,                               \
                    FIND_ALL_REGION_ID_ZIPCODE_SORTED_SQL,                     \
                    FIND_RESTAURANT_BY_RESTAURANT_ID,                          \
                    RECOMMEND_RESTAURANT_FOR_EVENT_BY_ID, CREATE_JOIN_SQL

from WebUtil import set_cookie_redirct, delete_existing_user_cookie

app = Flask(__name__)

#
# This line creates a database engine that knows how to connect to the URI above.
#

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
    context = dict()
    username = request.cookies.get('username')
    if username:
        context = dict(username = username)
    return render_template("index.html", **context)

@app.route('/test')
def test():
    return render_template("test_semantic.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form["email"]
        username = request.form["username"]
        cursor = g.conn.execute(LOGIN_USER_SQL, (username, email))
        result = get_first_result(cursor)
        if result:
            resp = make_response(redirect("/"))
            delete_existing_user_cookie(resp)
            resp.set_cookie('username', username)
            resp.set_cookie('email', email)
            resp.set_cookie('user_id', str(result[0]))
            return resp
        else:
            # TODO(Chris): Handle the not found case error message
            print "No such user!"
            region_cursor = g.conn.execute(FIND_ALL_REGION_ID_ZIPCODE_SORTED_SQL)
            region_tuples = get_results(region_cursor)
            regions = collect_regions(region_tuples)
            return render_template("sign_up.html", regions=regions)

@app.route('/sign_up', methods=["POST", "GET"])
def signup():
    try:
        region_cursor = g.conn.execute(FIND_ALL_REGION_ID_ZIPCODE_SORTED_SQL)
        region_tuples = get_results(region_cursor)
        regions = collect_regions(region_tuples)
        if request.method == "GET":
            return render_template("sign_up.html", regions=regions)
        else: # POST
            params = (request.form["username"], request.form["email"],             \
                        request.form["age"], request.form["gender"], request.form["zipcode"])
            g.conn.execute(SIGNUP_USER_SQL, params)
            cursor = g.conn.execute(GET_LAST_USER_ID_SQL)
            result = get_first_result(cursor)
            if cursor:
                resp = make_response(redirect("/"))
                delete_existing_user_cookie(resp)
                resp.set_cookie('username', request.form["username"])
                resp.set_cookie('email', request.form["email"])
                resp.set_cookie('user_id', str(result[0]))
                return resp
            else:
                # TODO(Chris): Handle the error format for signup,
                # ex. enter age with not numbers or some db callback
                print "Something happens in DB"
                return render_template("sign_up.html", regions=regions)
    except:
        return redirect("/")
'''
Restaurant Part:
- restaurant
- find_restaurants
- add_review
'''

def collect_features(feature_tuples):
    return [{'id': feature[0], 'name': feature[1]} for feature in feature_tuples]

def collect_regions(region_tuples):
    return [{'id': region[0], 'zipcode': region[1]} for region in region_tuples]

def collect_reviews(review_tuples):
    return [{'id': review[0], 'restaurant_name': review[1],                    \
            'addr': review[2], 'person_name': review[3],                       \
            'rate': int(review[4]), 'comment': review[5],                      \
            'date': review[6], }                                               \
            for review in review_tuples]

@app.route('/restaurant')
def restaurant():
    restaurant_id = request.args.get('restaurant_id')
    if restaurant_id:
        cursor = g.conn.execute(FIND_RESTAURANT_WITH_REVIEW_BY_ID,             \
                                                        restaurant_id)
        results = get_results(cursor)
        reviews = collect_reviews(results)

        rest_cursor = g.conn.execute(FIND_RESTAURANT_BY_RESTAURANT_ID,         \
                                        restaurant_id)
        rest_results = get_results(rest_cursor)
        rest = collect_restaurants(rest_results)
        return render_template("restaurant_review.html", reviews=reviews,      \
                                                            restaurants=rest)
    else:
        feature_cursor = g.conn.execute(FIND_ALL_FEATURES_SQL)
        region_cursor = g.conn.execute(FIND_ALL_REGION_ID_ZIPCODE_SQL)
        feature_tuples = get_results(feature_cursor)
        region_tuples = get_results(region_cursor)
        features = collect_features(feature_tuples)
        regions = collect_regions(region_tuples)
        return render_template("restaurant.html", features=features,           \
                                                    regions=regions)
@app.route('/add_review', methods=["POST"])
def add_review():
    rate = request.form["rate"]
    comment = request.form["comment"]
    restaurant_id = request.form["restaurant_id"]
    user_id = request.cookies.get("user_id")
    date = datetime.now().strftime("%Y-%m-%d")
    if not user_id:
        return redirect('/')
    g.conn.execute(ADD_REVIEW_SQL, (restaurant_id, user_id, comment, date, rate))
    return redirect(url_for("restaurant", restaurant_id=restaurant_id))

def collect_restaurants(restaurant_tuples):
    return [{'id': restaurant[0], 'name': restaurant[1],                       \
            'addr': restaurant[2], 'location': restaurant[4],                  \
            'rate': round(restaurant[5], 2), 'star': int(restaurant[5]),       \
            'rcount': restaurant[6]}                                           \
            for restaurant in restaurant_tuples]

@app.route('/find_restaurants', methods=["POST"])
def find_restaurants():
    zipcode = request.form["zipcode"]
    feature_id = request.form["feature_id"]
    if not (zipcode or feature_id):
        return redirect("/restaurant")
    else:
        if zipcode and feature_id:
            cursor = g.conn.execute(FIND_RESTAURANT_BY_ZIPCODE_AND_FEATURE, (feature_id, zipcode))
        elif feature_id:
            cursor = g.conn.execute(FIND_RESTAURANT_BY_FEATURE, feature_id)
        else:
            cursor = g.conn.execute(FIND_RESTAURANT_BY_ZIPCODE, zipcode)
        results = get_results(cursor)
        restaurants = collect_restaurants(results)
        return render_template("restaurant_results.html", restaurants=restaurants)

'''
Event Part:
- event
    - with event_id
    - without event_id
- create_event
- join_event
'''

def collect_events(event_tuples):
    if event_tuples:
        if len(event_tuples[0]) == 6:
            return [{'id':  event[0],                                                  \
                     'name': event[1],                                                 \
                     'desc': event[2],                                                 \
                     'time': datetime.combine(event[3], event[4])                      \
                                     .strftime("%Y-%m-%d %H:%M:%S"),                   \
                     'number': event[5]}                                               \
                     for event in event_tuples]
        else:
            return [{'id':  event[0],                                                  \
                     'name': event[1],                                                 \
                     'desc': event[2],                                                 \
                     'time': datetime.combine(event[3], event[4])                      \
                                     .strftime("%Y-%m-%d %H:%M:%S")}                   \
                     for event in event_tuples]
    return event_tuples

@app.route('/event')
def event():
    event_id = request.args.get("event_id")
    event_owner = request.args.get("event_owner")
    if event_id:
        event_cursor = g.conn.execute(FIND_EVENT_WITH_ID_SQL, event_id)
        event = get_first_result(event_cursor)
        restaurant_cursor = g.conn.execute                                     \
                            (RECOMMEND_RESTAURANT_FOR_EVENT_BY_ID, event_id)
        restaurants = collect_restaurants(get_results(restaurant_cursor))
        event_dict = dict(name=event[1], desc=event[2],                        \
                          datetime=datetime.combine(event[3], event[4])        \
                                            .strftime("%Y-%m-%d %H:%M:%S"),    \
                          event_id=event_id, event_owner=event_owner,          \
                          restaurants=restaurants)
        return render_template("event.html", **event_dict)
    else:
        user_id = request.cookies.get("user_id")
        own_cursor = g.conn.execute(FIND_USER_OWN_EVENTS_SQL, user_id)
        join_cursor = g.conn.execute(FIND_USER_JOIN_EVENTS_SQL, user_id)
        own_events = get_results(own_cursor)
        join_events = get_results(join_cursor)
        data = dict(own_events=collect_events(own_events),                     \
                    join_events=collect_events(join_events))
        return render_template("user_events.html", **data)

@app.route('/create_event', methods=["GET", "POST"])
def create_event():
    if request.method == "GET":
        return render_template("create_event.html")
    else: # POST
        event_date, event_time = request.form["event_time"].split(" - ")
        event_params = request.form["event_name"],                             \
                       request.form["event_desc"],                             \
                       event_date, event_time
        g.conn.execute(CREATE_EVENT_SQL, event_params)
        g.conn.execute(CREATE_OWN_SQL, request.cookies.get("user_id"))
        g.conn.execute(CREATE_JOIN_SQL, request.cookies.get("user_id"))
        return redirect("/event")

@app.route('/browse_event')
def browse_event():
    user_id = request.cookies.get("user_id")
    cursor = g.conn.execute(FIND_EVENTS_USER_NOT_IN_SQL, (user_id, user_id))
    results = get_results(cursor)
    events = collect_events(results)
    return render_template("other_events.html", events=events)

@app.route('/join_event', methods=["POST"])
def join_event():
    event_id = request.form["event_id"]
    user_id = request.cookies.get("user_id")
    g.conn.execute(JOIN_EVENT_SQL, (event_id, user_id))
    return redirect("/event")

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
