from flask import Flask
from src.config import ConfigDev, CustomJSONProvider
# from src.models import db
from src.routes import scraping_bp
# from src.auth import configure_jwt
# from src.routes import auth_bp
# from src.docs import configure_swagger

app = Flask(__name__)
app.config.from_object(ConfigDev)
# db.init_app(app)
# configure_jwt(app)
app.json = CustomJSONProvider(app)
app.register_blueprint(scraping_bp)
# app.register_blueprint(auth_bp)
# configure_swagger(app)


@app.route('/')
def home():
    return "Welcome to Embrapa's API"

if __name__ == '__main__':
    app.run(debug=True)