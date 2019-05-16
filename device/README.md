# Device software

## Configure WiFi connection
1. Connect to arduino WiFi network.
2. Go to [http://192.168.240.1/](http://192.168.240.1/).
3. Configure your wifi network. Note the assigned IP address.
4. Disconnect from the arduinos network.
5. Connect to th network configured in step 3.

Arduino should be accessible at an adress noted in step 3.


## Arduino Uno WiFi Developer Edition
This version of arduino has some serious design flaws and support is discontinued. What is more, documentation was lost in the proces of merging arduino.org and arduino.cc companies. Thes notes might be halpful to mke it work on your own. This repository containes `libraries` folder that has the development library missing from the official repository, essential to make the WiFi functionality work.

### Known issues
The Ciao.write/Ciao.read functions are not able to parse http response body. Thus, the device has to act like a queryable server, not pushing device.

### Essential links
1. Library that you have to install manually to Arduino IDE, to make anything work, also these are only working examples on the web
https://github.com/arduino-org/arduino-library-arduino-wifi
2. Essential documentation - in the internet archive!
https://web.archive.org/web/20170717121950/http://www.arduino.org:80/products/boards/arduino-uno-wifi
3. Someone's struggle to make it work with blynk
https://community.blynk.cc/t/solved-new-arduino-uno-wifi-board/6563/45
4. Updating WiFi chip firmware
https://store.arduino.cc/arduino-uno-wifi

