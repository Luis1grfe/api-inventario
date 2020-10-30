from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    apellido = db.Column(db.String(120), unique=False, nullable=False)
    empresa = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    telefono = db.Column(db.String(12), unique=False, nullable=False)
    datos = db.Column(db.Text, unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "empresa": self.empresa,
            "email": self.email,
            "telefono": self.telefono,
            "datos": self.datos
            # do not serialize the password, its a security breach
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    des = db.Column(db.String(240), unique=False, nullable=False)
    paleta = db.Column(db.Integer, unique=False, nullable=False)
    cantidaddebotellas = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "des": self.des,
            "paleta": self.paleta,
            "cantidaddebotellas": self.cantidaddebotellas
            # do not serialize the password, its a security breach
        }

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, unique=True, nullable=False)
    producto = db.Column(db.String(120), unique=False, nullable=False)
    cantidad = db.Column(db.Integer, unique=False, nullable=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)
    fecha = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return '<Inventario %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "fecha": self.fecha
            # do not serialize the password, its a security breach
        }