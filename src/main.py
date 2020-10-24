"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Product
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# All products list
@app.route('/list', methods=['GET'])
def handle_list():

    list_query = Product.query.all()
    all_product = list(map(lambda x: x.serialize(), list_query))

    return jsonify(all_product), 200

#Product insert in database
@app.route('/add', methods=['POST'])
def handle_add():
    decoded_object = json.loads(request.data)
    new_product = Product(sku=decoded_object["sku"], name=decoded_object["name"], paleta=decoded_object["paleta"], cantidaddebotellas=decoded_object["cantidaddebotellas"])
    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.serialize()), 200

#Product delete

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
