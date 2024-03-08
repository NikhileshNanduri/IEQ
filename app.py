from flask import Flask
import os
from flask_jwt_extended import JWTManager
from routes import authentication, products, users
from config import JWT_SECRET_KEY

app = Flask(__name__)

# Set up JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # Change this to a secure secret key in production
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(authentication.bp)
app.register_blueprint(products.bp)
app.register_blueprint(users.bp)

@app.route('/', methods=['GET'])
def home_page():
    return "Interactive EQ Assessment"


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', default=4000))
    app.run(debug=True, host='0.0.0.0' , port=port)