from flask import Flask
from routes import init_routes
from db import init_db
from flask_cors import CORS
# from flask import make_response

app = Flask(__name__)


CORS(app)


# Initialize configuration and database
app.config.from_object('config.Config')
init_db(app)

# Register routes (BluePrints)
init_routes(app)

# @app.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins (change as needed)
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     return response

if __name__ == '__main__':
    app.run(debug=True)
