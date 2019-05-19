import requests
import json
import time

# Endpoints
#http://192.168.5.18
ARDUINO_DATA_GET = '/arduino/digital/data'
ARDUINO_STATUS_GET = '/arduino/digital/status'
ARDUINO_OPEN_REQUEST = '/arduino/digital/open'
ARDUINO_CLOSE_REQUEST = '/arduino/digital/close'

API_NEWDATA_POST = 'http://localhost:5000/data/newdata'
API_ALL_DEVICES = 'http://localhost:5000/devices/all'

# Params
headers = {'Content-Type': 'application/json',}
timeout = 20
MODE = 'automatic' # 'manual
# Threasholds
TEMP_LIMIT = 10.0 # close if < limit
SOUND_LIMIT = 465 # close if > limit
'''
def close_request_by_limits(temp, sound):
    if ((temp <= TEMP_LIMIT) or (sound >= SOUND_LIMIT)):
        return "close"
    else:
        return None
'''

def parse_sensor_data(arduino_data, arduino_status):
    mydict = {}
    mylist = arduino_data.text.split(',')
    mydict['temp'] = float(mylist[3])
    mydict['hum'] = int(mylist[2])
    mydict['sound'] = int(mylist[1])
    mydict['gas'] = int(mylist[0])
    mydict['open_status'] = arduino_status.text
    return mydict


if __name__ == '__main__':
    devices_json = requests.get(API_ALL_DEVICES).text
    devices = json.loads(devices_json) # list of dics
    while(True):
        for device in devices:
            IP = device['ip_address']
            device_id = device['id']
            data = requests.get(IP+ARDUINO_DATA_GET, timeout = timeout)
            status = requests.get(IP+ARDUINO_STATUS_GET, timeout = timeout)
            new_data_dict = parse_sensor_data(data, status)
            new_data_dict['device_id'] = device_id
            new_data = json.dumps(new_data_dict)
            print(new_data)
            new = requests.post(url = API_NEWDATA_POST, headers = headers, data = new_data)
            '''
            if (MODE == "automatic"):
                if (close_request_by_limits(new_data_dict['temp'], new_data_dict['sound']) is not None):
                    requests.get(ARDUINO_CLOSE_REQUEST, timeout = timeout)
        '''
        time.sleep(50)