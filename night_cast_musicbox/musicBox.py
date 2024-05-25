from flask import Flask, render_template, request, jsonify
import pychromecast
import requests
import zeroconf

app = Flask(__name__)

# Jellyfin configuration
JELLYFIN_ADDRESS = 'http://192.168.2.96:8096'
JELLYFIN_API = '6d21cffd2399437f95b6cc85589778a3'
USER_ID = 'Chromcasting'  # Update this with the actual Jellyfin User ID

# Discover Chromecast devices
class CastListener:
    def __init__(self):
        self.devices = {}

    def add_cast(self, uuid, service):
        self.devices[uuid] = service

# Initialize zeroconf and start discovery
zconf = zeroconf.Zeroconf()
listener = CastListener()
browser = pychromecast.CastBrowser(listener, zconf)
browser.start_discovery()

# Stop discovery after a delay
import time
time.sleep(5)
browser.stop_discovery()
zconf.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playlists', methods=['GET'])
def get_playlists():
    url = f"{JELLYFIN_ADDRESS}/Users/{USER_ID}/Items?IncludeItemTypes=Playlist"
    headers = {'X-Emby-Token': JELLYFIN_API}
    response = requests.get(url, headers=headers)
    playlists = response.json().get('Items', [])
    return jsonify(playlists)

@app.route('/chromecasts', methods=['GET'])
def get_chromecasts():
    devices = [service.friendly_name for service in listener.devices.values()]
    return jsonify(devices)

@app.route('/cast', methods=['POST'])
def cast_playlist():
    data = request.json
    playlist_id = data['playlist_id']
    google_mini_name = data['google_mini_name']

    # Get playlist content
    url = f"{JELLYFIN_ADDRESS}/Users/{USER_ID}/Items?ParentId={playlist_id}"
    headers = {'X-Emby-Token': JELLYFIN_API}
    response = requests.get(url, headers=headers)
    items = response.json().get('Items', [])

    if not items:
        return jsonify({'status': 'error', 'message': 'No tracks found in playlist'}), 404
    
    # Get URL of the first item in the playlist
    media_url = f"{JELLYFIN_ADDRESS}/Audio/{items[0]['Id']}/stream.mp3?api_key={JELLYFIN_API}"

    # Find Chromecast device and connect
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[google_mini_name])
    if not chromecasts:
        return jsonify({'status': 'error', 'message': f"No Chromecast with name {google_mini_name} found"}), 404
    
    cast = chromecasts[0]
    cast.wait()

    # Cast media
    cast.media_controller.play_media(media_url, 'audio/mpeg')
    cast.media_controller.block_until_active()

    return jsonify({'status': 'success', 'message': 'Your selection is playing on the selected Google Mini'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
