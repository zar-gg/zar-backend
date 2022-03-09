from riot_client import RiotClient
from flask import Flask, request
from flask_caching import Cache
from flask_cors import CORS
import json

config = {
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)
CORS(app, send_wildcard=True)

rc = RiotClient()

@app.route("/server-status", methods=["GET"])
def server_status():
    return {"status": "OK", "code": 200}

@app.route("/get-player/<player_name>", methods=["GET"])
# @cache.memoize(timeout=90)
def get_player(player_name):
    print('Calling riot api')
    return rc.get_player(request.args.get('region'), 
                         player_name)

@app.route("/get-players/<key>", methods=["GET"])
# @cache.memoize(timeout=90)
def get_players(key):
    return rc.get_players(request.args.get('region'),
                         key)

@app.route("/get-ranked-stats/<player_id>", methods=["GET"])
# @cache.memoize(timeout=90)
def get_ranked_stats(player_id):
    return json.dumps(rc.get_ranked_stats(request.args.get('region'), 
                                          player_id))

@app.route("/match-history/<puuid>", methods=["GET"])
# @cache.memoize(timeout=90)
def get_matches(puuid):
    return json.dumps(rc.get_match_history(request.args.get('region', 'euw'), puuid,
                                           request.args.get('queue', None), 
                                           request.args.get('count', 50)))

@app.route("/clash-details", methods=["GET"])
# @cache.cached(timeout=90)
def clash_details():
    return json.dumps(rc.get_clash_details(request.args.get('region')))


if __name__ == '__main__':
    
    from dotenv import load_dotenv

    load_dotenv()
    app.run("0.0.0.0", port=8000, debug=True)
