from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    paleta = db.Column(db.Integer, unique=True, nullable=False)
    cantidaddebotellas = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "paleta": self.paleta,
            "cantidaddebotellas": self.cantidaddebotellas
            # do not serialize the password, its a security breach
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    paleta = db.Column(db.Integer, unique=False, nullable=False)
    cantidaddebotellas = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "paleta": self.paleta,
            "cantidaddebotellas": self.cantidaddebotellas
            # do not serialize the password, its a security breach
        }