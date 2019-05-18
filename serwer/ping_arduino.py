import requests
import json
import time

# Endpoints
ARDUINO_DATA_GET = 'http://192.168.5.18/arduino/digital/data'
ARDUINO_STATUS_GET = 'http://192.168.5.18/arduino/digital/status'
API_NEWDATA_POST = 'http://localhost:5000/data/newdata'
ARDUINO_OPEN_REQUEST = 'http://192.168.5.18/arduino/digital/open'
ARDUINO_CLOSE_REQUEST = 'http://192.168.5.18/arduino/digital/close'

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
    if arduino_status.text == 'open':
        mydict['open_status'] = True
    else:
        mydict['open_status'] = False
    return mydict, json.dumps(mydict)


if __name__ == '__main__':
    while(True):
        data = requests.get(ARDUINO_DATA_GET, timeout = timeout)
        status = requests.get(ARDUINO_STATUS_GET, timeout = timeout)
        new_data_dict, new_data = parse_sensor_data(data, status)
        print(new_data)
        new = requests.post(url = API_NEWDATA_POST, headers = headers, data = new_data)
        '''
        if (MODE == "automatic"):
            if (close_request_by_limits(new_data_dict['temp'], new_data_dict['sound']) is not None):
                requests.get(ARDUINO_CLOSE_REQUEST, timeout = timeout)
        '''
        time.sleep(50)