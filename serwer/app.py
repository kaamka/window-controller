from flask import Flask, request, jsonify, logging
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import datetime
import requests
from sqlalchemy.orm import sessionmaker

ARDUINO = 'http://192.168.5.18'
ARDUINO_DATA_GET = '/arduino/digital/data'
ARDUINO_STATUS_GET = '/arduino/digital/status'
ARDUINO_OPEN_REQUEST = '/arduino/digital/open'
ARDUINO_CLOSE_REQUEST = '/arduino/digital/close'
timeout = 10

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


# create a configured "Session" class
Session = sessionmaker(bind=db)
# create a Session
session = Session()


# SensorsData Class/Model
class SensorsData(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
  device = db.relationship('Device',backref=db.backref('sensors_data', lazy=True))
  time = db.Column(db.DateTime, default=datetime.datetime.now())
  temp= db.Column(db.Float)
  hum = db.Column(db.Integer)
  sound = db.Column(db.Integer)
  gas = db.Column(db.Integer)
  open_status = db.Column(db.String(10))

  def __init__(self, device_id, temp, hum, sound, gas, open_status):
    self.device_id = device_id
    self.temp = temp
    self.hum = hum
    self.sound = sound
    self.gas = gas
    self.open_status = open_status

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    def __init__(self, name, ip_address):
        self.name = name
        self.ip_address = ip_address

    def __repr__(self):
        return '<Device %r : %r>' % self.name, self.ip_address


# Sensor data Schema
class SensorsDataSchema(ma.Schema):
  class Meta:
    fields = ('id', 'device_id', 'time', 'temp', 'hum', 'sound', 'gas', 'open_status')

# Init schema
sensors_data_schema = SensorsDataSchema(strict=True)
sensors_history_schema = SensorsDataSchema(many=True, strict=True)


# Devices Schema
class DeviceSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'ip_address')

# Init devices schema
device_schema = DeviceSchema(strict=True)
all_devices_schema = DeviceSchema(many=True, strict=True)


# Home
@app.route('/', methods=['GET'])
def hello():
    return jsonify({'msg': 'Hello Arduino'})

# Add the device
@app.route('/devices/new', methods=['POST'])
def add_device():
  name = request.json['name']
  ip_address = request.json['ip_address']
  new_device = Device(name, ip_address)

  db.session.add(new_device)
  db.session.commit()

  return device_schema.jsonify(new_device)


# Add the data
@app.route('/data/newdata', methods=['POST'])
def add_data():
  device_id = request.json['device_id']
  temp = request.json['temp']
  hum = request.json['hum']
  sound = request.json['sound']
  gas = request.json['gas']
  open_status = request.json['open_status']

  new_data = SensorsData(device_id, temp, hum, sound, gas, open_status)

  db.session.add(new_data)
  db.session.commit()

  return sensors_data_schema.jsonify(new_data)


# Get History
@app.route('/data/all', methods=['GET'])
def get_history():
  history = SensorsData.query.all()
  result = sensors_history_schema.dump(history)
  return jsonify(result.data)

# Get history of one device
#sensors_data
@app.route('/data/all/<device_id>', methods=['GET'])
def get_data_of_device(device_id):
  r = SensorsData.query.filter_by(device_id = device_id)
  result = sensors_history_schema.dump(r)
  return jsonify(result.data)

# Get Single data record
@app.route('/data/<id>', methods=['GET'])
def get_data_by_id(id):
  data = SensorsData.query.get(id)
  return sensors_data_schema.jsonify(data)

# Get All Devices
@app.route('/devices/all', methods=['GET'])
def get_all_devices():
  devices = Device.query.all()
  result = all_devices_schema.dump(devices)
  return jsonify(result.data)

# Get Single Device
@app.route('/devices/<id>', methods=['GET'])
def get_device_by_id(id):
  data = Device.query.get(id)
  return device_schema.jsonify(data)


# Update a Device
@app.route('/devices/<id>', methods=['PUT'])
def update_device(id):
  dev = Device.query.get(id)
  name = request.json['name']
  ip_address = request.json['ip_address']
  dev.name = name
  dev.ip_address = ip_address
  db.session.commit()
  return device_schema.jsonify(dev)

# Delete data
@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
  data = SensorsData.query.get(id)
  db.session.delete(data)
  db.session.commit()
  return sensors_data_schema.jsonify(data)

# Delete device 
@app.route('/devices/<id>', methods=['DELETE'])
def delete_device_by_id(id):
  data = Device.query.get(id)
  db.session.delete(data)
  db.session.commit()
  return device_schema.jsonify(data)


# Get status
@app.route('/data/latest/status/<device_id>', methods=['GET'])
def get_status(device_id):
    last_record = SensorsData.query.filter_by(device_id = device_id).order_by(SensorsData.id.desc()).first()
    return str(last_record.open_status)

'''
# Get the latest data of all devices
@app.route('/data/latest', methods=['GET'])
def get__all_latest_data():
    data = session.query(Device.id).join(SensorsData.open_status)
    return str(data.text)
# Get the latest statuses of all devices
'''

# Get latest data
@app.route('/data/latest/<device_id>', methods=['GET'])
def get_latest_data(device_id):
    last_record = SensorsData.query.filter_by(device_id = device_id).order_by(SensorsData.id.desc()).first()
    return sensors_data_schema.jsonify(last_record)


# Change status to open
@app.route('/open/<device_id>', methods=['GET'])
def open_request(device_id):
    dev = Device.query.get(device_id)
    url = dev.ip_address + ARDUINO_OPEN_REQUEST
    arduino_response = requests.get(url, timeout = timeout)
    return str(arduino_response.text)


# Change status to close
@app.route('/close/<device_id>', methods=['GET'])
def close_request(device_id):
    dev = Device.query.get(device_id)
    url = dev.ip_address + ARDUINO_CLOSE_REQUEST
    arduino_response = requests.get(url, timeout = timeout)
    return str(arduino_response.text)


# Change status to close for all devices

# Change status to close for all devices
'''
# Change mode to automatic
@app.route('/mode/auto', methods=['GET'])
def set_auto_mode():
    arduino_response = requests.get(ARDUINO_AUTO_REQUEST, timeout = timeout)
    return str(arduino_response.text)


# Change mode to manual
@app.route('/mode/manual', methods=['GET'])
def set_manual_mode():
    arduino_response = requests.get(ARDUINO_MANUAL_REQUEST, timeout = timeout)
    return str(arduino_response.text)
'''

# Run server
if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', True), host='0.0.0.0')