# 1. import Flask
# from flask import Flask
# from flask import jsonify

# # 2. Create an app, being sure to pass __name__
# app = Flask(__name__)


# # 3. Define what to do when a user hits the index route
# # route will tell the server based on the clients choice 
# # what to return, it is basically the menu
# # Flask Routes
# @app.route("/")
# def home():
#     print("My Trip Precipitacion")
#     return "I was lucky, I encountered little rain"


# # 4. Define what to do when a user hits the /about route
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     return (
#         f"Welcome to the Justice League API!<br/>"
#         f"Available Routes:<br/>"
#         f"/api/v1.0/justice-league<br/>"
#         f"/api/v1.0/justice-league/superhero/batman"
#     )

# # 5. Define what to do when a user hits the /about route
# @app.route("/contact")
# def contact():
#     print("Server received request for 'Contact' page...")
#     return "Please email me at mery@mypage.com"


# if __name__ == "__main__":
#     app.run(debug=True)


# #-------------------------------------------

# hello_dict = {"Hello": "World!"}
# hello_str = "Hello World"

# @app.route("/")
# def home():
#     return "Hi"

# @app.route("/normal")
# def normal():
#     return hello_str

# @app.route("/jsonified")
# def jsonified():
#     return jsonify(hello_dict)

# if __name__ == "__main__":
#     app.run(debug=True)    

# #------------------------------------

# from flask import Flask, jsonify

# justice_league_members = [
#     {"superhero": "Aquaman", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

# # Flask Setup
# app = Flask(__name__)


# # Flask Routes
# @app.route("/api/v1.0/precipitation")
# def justice_league():
#     """Return the justice league data as json"""

#     return jsonify(justice_league_members)


# @app.route("/")
# def welcome():
#     return (
#         f"Welcome to the Justice League API!<br/>"
#         f"Available Routes:<br/>"
#         f"/api/v1.0/justice-league<br/>"
#         f"/api/v1.0/justice-league/Arthur%20Curry<br/>"
#         f"/api/v1.0/justice-league/Bruce%20Wayne<br/>"
#         f"/api/v1.0/justice-league/Victor%20Stone<br/>"
#         f"/api/v1.0/justice-league/Barry%20Allen<br/>"
#         f"/api/v1.0/justice-league/Hal%20Jordan<br/>"
#         f"/api/v1.0/justice-league/Clark%20Kent/Kal-El<br/>"
#         f"/api/v1.0/justice-league/Princess%20Diana"
#     )


# @app.route("/api/v1.0/justice-league/<real_name>")
# def justice_league_character(real_name):
#     """Fetch the Justice League character whose real_name matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = real_name.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


# if __name__ == "__main__":
#     app.run(debug=True)

# # -----------------------------------------------

# from flask import Flask, jsonify

# justice_league_members = [
#     {"superhero": "Aquaman", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

# #################################################
# # Flask Setup
# #################################################
# app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

# @app.route("/api/v1.0/justice-league")
# def justice_league():
#     """Return the justice league data as json"""

#     return jsonify(justice_league_members)


# @app.route("/")
# def welcome():
#     return (
#         f"Welcome to the Justice League API!<br/>"
#         f"Available Routes:<br/>"
#         f"/api/v1.0/justice-league<br/>"
#         f"/api/v1.0/justice-league/superhero/batman"
#     )


# """TODO: Handle API route with variable path to allow getting info
# for a specific character based on their 'superhero' name """

# @app.route("/api/v1.0/justice-league/<superhero>")
# def justice_league_character(superhero):
#     """Fetch the Justice League character whose real_name matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = superhero.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["superhero"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {superhero} not found."}), 404


# if __name__ == "__main__":
#     app.run(debug=True)

# --------------------------------------------------
#     
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""
    # Query all precipitation
    # results = session.query(Passenger.name).all()

    # # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    # return jsonify(all_names)

    mdates = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    query_date_yearago = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    return jsonify(all_names)

# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
