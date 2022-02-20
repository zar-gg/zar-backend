from riot_client import RiotClient
from flask import Flask, request
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()
rc = RiotClient()
    
@app.route("/server-status")
def server_status():
    return {"status": "OK", "code": 200}

@app.route("/get-player")
def get_player():
    return rc.get_player(request.args.get('region'), request.args.get('name'))

@app.route("/clash-details")
def clash_details():
    return json.dumps(rc.get_clash_details(request.args.get('region')))

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)