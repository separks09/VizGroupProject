from flask import Flask, jsonify, render_template, url_for
import pandas as pd
import numpy as np
import os

import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date
import json


#Connecting to sqlite database
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)


@app.before_first_request
def setup():
    db.drop_all()
    db.create_all()

@app.route("/")
def index():
    return render_template('chart.html')

@app.route("/pass_yards")
def pass_yds():
    return render_template('pass_yards.html')

@app.route("/rush_yards")
def rush_yds():
    return render_template('rush_yards.html')

@app.route('/data.json')
def testdb():
    Base=declarative_base()
    engine= create_engine('sqlite:///nfldata.sqlite',echo=False) 
    class NFLdata(Base):
        __tablename__='NFLdata'
        teamseason=Column('teamseason',String, primary_key=True)
        opp_pass_yd=Column('opp_pass_yd',String)
        opp_rush_yds=Column('opp_rush_yds',String)
        pass_yds=Column('pass_yds',String)
        rush_yds=Column('rush_yds',String)
        pts=Column('pts',String)
        pts_against=Column('pts_against',String)
        season=Column('season',String)
        takeaways=Column('takeaways',String)
        team=Column('team',String)
        turnovers=Column('turnovers',String)
        win=Column('win', String)
    Session=sessionmaker(bind=engine)
    session=Session()
    users=session.query(NFLdata).all()
    session.close()
    opp_pass_yd=[]
    opp_rush_yds=[]
    pass_yds=[]
    pts=[]
    pts_against=[]
    rush_yds=[]
    season=[]
    takeaways=[]
    team=[]
    turnovers=[]
    win=[]
    teamseason=[]
    for user in users:
        opp_pass_yd.append(int(user.opp_pass_yd))
        opp_rush_yds.append(int(user.opp_rush_yds))
        pass_yds.append(int(user.pass_yds))
        pts.append(int(user.pts))
        pts_against.append(int(user.pts_against))
        rush_yds.append(int(user.rush_yds))
        season.append(int(user.season))
        takeaways.append(int(user.takeaways))
        team.append(user.team)
        turnovers.append(int(user.turnovers))
        win.append(int(user.win))
        teamseason.append(user.teamseason)
    a=pd.DataFrame({'teamseason':teamseason,'team':team,'season':season,'pass_yds':pass_yds,'rush_yds':rush_yds,'opp_pass_yds':opp_pass_yd,'opp_rush_yds':opp_rush_yds,'pts':pts,'pts_against':pts_against,'takeaways':takeaways,'turnovers':turnovers,'win':win})
    listofstats=[i for i in a]
    listofteams=[i for i in a.groupby('team').groups.keys()]
    listofseasons=[i for i in a.groupby('season').groups.keys()]
    del(listofstats[-3])
    del(listofstats[-3])
    finaljson=[]
    for team in listofteams:
        teamdictionary={}
        teamdictionary['team']=team
        for stat in listofstats:
            statlist=[]
            for index in range(len(a['season'])):
                if a['team'][index]==team:
                    statlist.append([int(a['season'][index]),int(a[stat][index])])
            teamdictionary[stat]=statlist
        finaljson.append(teamdictionary)
    return jsonify(finaljson)

@app.route('/table')
def table():
    
    Base=declarative_base()
    engine= create_engine('sqlite:///nfldata.sqlite',echo=False) 
    class NFLdata(Base):
        __tablename__='NFLdata'
        teamseason=Column('teamseason',String, primary_key=True)
        opp_pass_yd=Column('opp_pass_yd',String)
        opp_rush_yds=Column('opp_rush_yds',String)
        pass_yds=Column('pass_yds',String)
        rush_yds=Column('rush_yds',String)
        pts=Column('pts',String)
        pts_against=Column('pts_against',String)
        season=Column('season',String)
        takeaways=Column('takeaways',String)
        team=Column('team',String)
        turnovers=Column('turnovers',String)
        win=Column('win', String)
    Session=sessionmaker(bind=engine)
    session=Session()
    users=session.query(NFLdata).all()
    session.close()
    opp_pass_yd=[]
    opp_rush_yds=[]
    pass_yds=[]
    pts=[]
    pts_against=[]
    rush_yds=[]
    season=[]
    takeaways=[]
    team=[]
    turnovers=[]
    win=[]
    teamseason=[]
    for user in users:
        opp_pass_yd.append(int(user.opp_pass_yd))
        opp_rush_yds.append(int(user.opp_rush_yds))
        pass_yds.append(int(user.pass_yds))
        pts.append(int(user.pts))
        pts_against.append(int(user.pts_against))
        rush_yds.append(int(user.rush_yds))
        season.append(int(user.season))
        takeaways.append(int(user.takeaways))
        team.append(user.team)
        turnovers.append(int(user.turnovers))
        win.append(int(user.win))
        teamseason.append(user.teamseason)
    a={'teamseason':teamseason,'team':team,'season':season,'pass_yds':pass_yds,'rush_yds':rush_yds,'opp_pass_yds':opp_pass_yd,'opp_rush_yds':opp_rush_yds,'pts':pts,'pts_against':pts_against,'takeaways':takeaways,'turnovers':turnovers,'win':win}
    return jsonify(a)


if __name__ == "__main__":
    app.run(debug=True)
