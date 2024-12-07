from flask import Flask
from routes import init_routes
from db import init_db
from flask_cors import CORS

app = Flask(__name__)


CORS(app)


# Initialize configuration and database
app.config.from_object('config.Config')
init_db(app)

# Register routes (BluePrints)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)