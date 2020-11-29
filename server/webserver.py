from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json

class WebApp:

    app = None

    def __init__(self, games_pool):
        pool = games_pool
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/get_all', methods=['GET'])
        def search():
            return json.dumps(games_pool)
            # data = request.args.get("name")
            # output = select_all_items(c, data)
            # return json.dumps(output)

