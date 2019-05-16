from flask import Flask, request, jsonify, logging
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import datetime

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class SensorsData(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  time = db.Column(db.DateTime, default=datetime.datetime.now())
  temp= db.Column(db.Float)
  hum = db.Column(db.Integer)
  sound = db.Column(db.Integer)
  gas = db.Column(db.Integer)
  open_status = db.Column(db.Boolean)

  def __init__(self, temp, hum, sound, gas, open_status):
    self.temp = temp
    self.hum = hum
    self.sound = sound
    self.gas = gas
    self.open_status = open_status


# Sensor data Schema
class SensorsDataSchema(ma.Schema):
  class Meta:
    fields = ('id', 'time', 'temp', 'hum', 'sound', 'gas', 'open_status')

# Init schema
sensors_data_schema = SensorsDataSchema(strict=True)
sensors_history_schema = SensorsDataSchema(many=True, strict=True)


# Home
@app.route('/', methods=['GET'])
def hello():
    return jsonify({'msg': 'Hello Arduino'})

# Add the data
@app.route('/newdata', methods=['POST'])
def add_data():
  temp = request.json['temp']
  hum = request.json['hum']
  sound = request.json['sound']
  gas = request.json['gas']
  open_status = request.json['open_status']

  new_data = SensorsData(temp, hum, sound, gas, open_status)

  db.session.add(new_data)
  db.session.commit()

  return sensors_data_schema.jsonify(new_data)

'''
# Get History
@app.route('/history', methods=['GET'])
def get_products():
  history = SensorsData.query.all()
  result = sensors_history_schema.dump(history)
  return jsonify(result.data)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()
  return product_schema.jsonify(product)
'''

# Run server
if __name__ == '__main__':
    app.run(debug=True)