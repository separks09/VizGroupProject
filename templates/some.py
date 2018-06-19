import datetime as dt
import numpy as np
import pandas as pd

from flask import (
   Flask,
   render_template,
   jsonify,
   request,
   redirect)

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# connect to engine

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)
Base = automap_base()

# Connect to Engine
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite.db")

# Reflect the tables 
Base.prepare(engine, reflect=True)

session = Session(engine)