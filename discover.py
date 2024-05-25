import time
import pychromecast
import zeroconf

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

# Cleanup
zconf.close()