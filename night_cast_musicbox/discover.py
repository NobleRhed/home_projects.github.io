# description: Testing on how to discover what chromecast devices are available on the network, and how to connect to them.

import time
import pychromecast
import zeroconf
import json
import os

# Create a listener class
class MyCastListener:
    def __init__(self):
        self.devices = []

    def add_cast(self, uuid, service):
        print(f"Found Chromecast device: {browser.devices[uuid].friendly_name}")
        self.devices.append(browser.devices[uuid].friendly_name)

# Initialize zeroconf
zconf = zeroconf.Zeroconf()
listener = MyCastListener()
browser = pychromecast.CastBrowser(listener, zconf)

# Start discovery
browser.start_discovery()
time.sleep(10)  # Allow some time for discovery
browser.stop_discovery()

# List discovered devices
print("Discovered Chromecast devices:")
for device in listener.devices:
    print(device)

# Define the file path for the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'chromecast_devices.json')

# Save discovered devices to a JSON file
with open(json_file_path, 'w') as f:
    json.dump(listener.devices, f)

# Cleanup
zconf.close()
