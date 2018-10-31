###########################################
# imports dependencies
###########################################
from datetime import datetime
from functools import singledispatch
from datetime import datetime as dt
from flask import Flask, Markup
import datetime
import time
import json
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,desc
import collections
from flask import Flask, jsonify

###########################################
# initializes database
###########################################

engine = create_engine("sqlite:///db/bk.db")
Base = automap_base()
Base.prepare(engine, reflect=True)

###########################################
# creates references to Info
# and Station tables
###########################################

Info = Base.classes.link

session = Session(engine)

####################################
# initializes Flask app
####################################
app = Flask(__name__)

################################
# initializes Flask Routes
################################
"""
"""
@singledispatch
def to_serializable(val):
    """Used by default."""
    return str(val)
    
@to_serializable.register(datetime)
def ts_datetime(val):
    """Used if *val* is an instance of datetime."""
    return val.isoformat() + "Z"


@app.route('/topten',methods = ['POST', 'GET'])
def topten():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))


@app.route('/success/<name>')
def success(name):
    foo = session.query(func.count(Info.Transection),Info.Item).\
    group_by(Info.Item).order_by(Info.Item).all()
    data2= json.dumps([{"date": foo[x][1],"value": foo[x][0]}
        for x in range(len(foo))],default=to_serializable)
    data={'chart_data':data2}
#   print(data)
    return render_template('index+js.html',data=data)


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Info).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    df["Item"] = df["Item"].str.strip()
    item_list = list(dict.fromkeys(df["Item"]))
    # Return a list of the item names
    return jsonify(item_list)

if __name__ == "__main__":
    app.run(debug=True)
