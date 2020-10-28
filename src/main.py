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
@app.route('/delete/<int:product_id>', methods=['DELETE'])
def handle_delete(product_id):
    product_delete = Product.query.get(product_id)
    if product_delete is None:
        raise APIException('Product not found', status_code=404)
    db.session.delete(product_delete)
    db.session.commit()

    return '',204

#Product Mod
@app.route('/mod/<int:product_id>', methods=['PUT'])
def handle_mod(product_id):
    body = json.loads(request.data)
    product_mod = Product.query.get(product_id)
    if product_mod is None:
        raise APIException('User not found', status_code=404)
    if "sku" in body:
        product_mod.sku = body["sku"]
    if "name" in body:
        product_mod.name = body["name"]
    if "paleta" in body:
        product_mod.paleta = body["paleta"]
    if "cantidaddebotellas" in body:
        product_mod.cantidaddebotellas = body["cantidaddebotellas"]
    db.session.commit()

    return jsonify(product_mod.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
