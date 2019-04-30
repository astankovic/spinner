from flask import Flask, request, jsonify, make_response
import json


class WebApp:

    app = None

    def __init__(self, games_pool):
        pool = games_pool
        self.app = Flask(__name__)

        @self.app.route('/search', methods=['GET'])
        def search():
            return 'Hello world'
            # data = request.args.get("name")
            # output = select_all_items(c, data)
            # return json.dumps(output)

