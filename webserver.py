from flask import Flask, request, jsonify, make_response
import json


class WebApp:
    def __init__(self, gamesPool):
        pool = gamesPool
        app = Flask(__name__)

        @app.route('/search', methods=['GET'])
        def search():
            return 'Hello world'
            # data = request.args.get("name")
            # output = select_all_items(c, data)
            # return json.dumps(output)

