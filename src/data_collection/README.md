# Data collection

Here lives code used to collect images.

## Video to images

Convert a video to a set of images using the `video_to_img.sh` script.

## ESP-EYE

Start a webserver on the ESP-EYE that streams camera footage over your network.
Make sure to configure your secrets, see the section below.
The implementation requires the Arduino IDE.
Configure the Arduino environment directly in the Arduino IDE or via the VSCode extension using keys `F1` or `CTRL+SHIFT+P`.

- Arduino: Select Serial Port. 
- Arduino: Board Config. Select AI Thinker ESP32-CAM.
- Arduino: Verify.
- Arduino: Open Serial Monitor.
- Arduino: Upload.
- Arduino: Change Baud Rate to 115200.

Now you can collect images manually, using the GUI, however this is very slow.

Start Selenium to open a browser and save images automatically.

    python3 src/data_collection/collect_from_esp.py

Note that this requires you to install Selenium and the according webdriver for your browser.
Some code adjustments to the Python script will likely be necessary.

### Configure secrets

Define a file `src/data_collection/credentials.h` with the following contents to connect the ESP-EYE to your network.
This will be necessary to collect data via WiFi.

    #ifndef CREDENTIALS_H

    #define CREDENTIALS_H
    #define WIFI_SSID "**********"
    #define WIFI_PW "*********"

    #endif