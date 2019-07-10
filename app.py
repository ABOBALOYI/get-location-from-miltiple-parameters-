import flask
from flask import request ,jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d




@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Invalid Url input.</p>", 404


@app.route('/api/location/', methods=['GET'])
def api_filter():
    query_parameters = request.args

  
    lon = query_parameters.get('lon')
    lat = query_parameters.get('lat')

    query = "SELECT OUTPUT FROM data_location WHERE"
    to_filter = []

    
    if lon:
        query += ' lon=? AND'
        to_filter.append(lon)
    if lat:
        query += ' lat=? AND'
        to_filter.append(lat)
    if not (lat and lon):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('location.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchone()

    return  jsonify(results)
app.run()