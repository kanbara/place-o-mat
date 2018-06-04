import logging

from flask import Flask, request, make_response, jsonify

from placeomat.providers import providers

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)


@app.route('/search')
@app.route('/search/<provider>')
def make_query(provider='all'):
    body, status = providers.query(provider, request.args.to_dict())
    return make_response((jsonify(body), status))


@app.route('/search/<provider>/<place_id>')
def get_place_details(provider, place_id):
    body, status = providers.place_id(provider, place_id)
    return make_response(jsonify(body), status)
