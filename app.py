from flask import Flask
from flask_restful import Api
from services.suggestion_service import Suggestion

app = Flask(__name__)

api = Api(app)

api.add_resource(Suggestion, "/suggestion")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
