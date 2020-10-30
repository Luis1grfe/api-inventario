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
from models import db, User, Product, Inventario
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

#Comienzo Route Producto
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
    new_product = Product(sku=decoded_object["sku"], name=decoded_object["name"],des=decoded_object["des"], paleta=decoded_object["paleta"], cantidaddebotellas=decoded_object["cantidaddebotellas"])
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
        raise APIException('Product not found', status_code=404)
    if "sku" in body:
        product_mod.sku = body["sku"]
    if "name" in body:
        product_mod.name = body["name"]
    if "des" in body:
        product_mod.name = body["des"]
    if "paleta" in body:
        product_mod.paleta = body["paleta"]
    if "cantidaddebotellas" in body:
        product_mod.cantidaddebotellas = body["cantidaddebotellas"]
    db.session.commit()

    return jsonify(product_mod.serialize()), 200

#Comienzo de route inventario
# All inventario list
@app.route('/inventario', methods=['GET'])
def handle_inventario():

    list_query = Inventario.query.all()
    all_inventario = list(map(lambda x: x.serialize(), list_query))

    return jsonify(all_inventario), 200

#Inventario insert in database
@app.route('/addinventario', methods=['POST'])
def handle_addinventario():
    decoded_object = json.loads(request.data)
    new_inventario = Inventario(sku=decoded_object["sku"], producto=decoded_object["producto"],cantidad=decoded_object["cantidad"], precio=decoded_object["precio"], fecha=decoded_object["fecha"])
    db.session.add(new_inventario)
    db.session.commit()

    return jsonify(new_inventario.serialize()), 200

#Inventario delete
@app.route('/deleteinventario/<int:inventario_id>', methods=['DELETE'])
def handle_deleteinventario(inventario_id):
    inventario_delete = Inventario.query.get(inventario_id)
    if inventario_delete is None:
        raise APIException('Inventario not found', status_code=404)
    db.session.delete(inventario_delete)
    db.session.commit()

    return '',204

#Inventario Mod
@app.route('/modinventario/<int:inventario_id>', methods=['PUT'])
def handle_modinventario(inventario_id):
    body = json.loads(request.data)
    inventario_mod = Inventario.query.get(inventario_id)
    if inventario_mod is None:
        raise APIException('Inventario not found', status_code=404)
    if "sku" in body:
        inventario_mod.sku = body["sku"]
    if "producto" in body:
        inventario_mod.name = body["producto"]
    if "cantidad" in body:
        inventario_mod.name = body["cantidad"]
    if "precio" in body:
        inventario_mod.paleta = body["precio"]
    if "fecha" in body:
        inventario_mod.cantidaddebotellas = body["fecha"]
    db.session.commit()

    return jsonify(inventario_mod.serialize()), 200

#Comienzo de route User
# All user list
@app.route('/user', methods=['GET'])
def handle_user():

    list_query = User.query.all()
    all_user = list(map(lambda x: x.serialize(), list_query))

    return jsonify(all_user), 200

#User insert in database
@app.route('/adduser', methods=['POST'])
def handle_adduser():
    decoded_object = json.loads(request.data)
    new_user = User(nombre=decoded_object["nombre"], apellido=decoded_object["apellido"],empresa=decoded_object["empresa"], email=decoded_object["email"], telefono=decoded_object["telefono"], datos=decoded_object["datos"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200

#USer delete
@app.route('/deleteuser/<int:user_id>', methods=['DELETE'])
def handle_deleteuser(user_id):
    user_delete = User.query.get(user_id)
    if user_delete is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user_delete)
    db.session.commit()

    return '',204

#User Mod
@app.route('/moduser/<int:user_id>', methods=['PUT'])
def handle_moduser(user_id):
    body = json.loads(request.data)
    user_mod = User.query.get(user_id)
    if user_mod is None:
        raise APIException('Inventario not found', status_code=404)
    if "nombre" in body:
        user_mod.sku = body["nombre"]
    if "apellido" in body:
        user_mod.name = body["apellido"]
    if "empresa" in body:
        user_mod.name = body["empresa"]
    if "email" in body:
        user_mod.paleta = body["email"]
    if "telefono" in body:
        user_mod.cantidaddebotellas = body["telefono"]
    if "datos" in body:
        user_mod.cantidaddebotellas = body["datos"]
    db.session.commit()

    return jsonify(user_mod.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
