import requests
import json

# Endpoints
ARDUINO_DATA_GET = 'http://192.168.5.18/arduino/digital/data'
ARDUINO_STATUS_GET = 'http://192.168.5.18/arduino/digital/status'
API_NEWDATA_POST = 'http://localhost:5000/newdata'
# Params
headers = {'Content-Type': 'application/json',}

def parse_sensor_data(arduino_data, arduino_status):
    mydict = {}
    mylist = arduino_data.text.split(',')
    mydict['temp'] = float(mylist[3])
    mydict['hum'] = int(mylist[2])
    mydict['sound'] = int(mylist[1])
    mydict['gas'] = int(mylist[0])
    if arduino_status.text == 'open':
        mydict['open_status'] = True
    else:
        mydict['open_status'] = False
    return json.dumps(mydict)


if __name__ == '__main__':
    data = requests.get(ARDUINO_DATA_GET)
    status = requests.get(ARDUINO_STATUS_GET)
    new_data = parse_sensor_data(data, status)
    print(new_data)
    new = requests.post(url = API_NEWDATA_POST, headers = headers, data = new_data)
