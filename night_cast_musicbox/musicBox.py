from flask import Flask, render_template, request, jsonify
import pychromecast
import requests
import zeroconf
import time

app = Flask(__name__)

# Jellyfin configuration
JELLYFIN_ADDRESS = 'http://192.168.2.96:8096'
JELLYFIN_API = '6d21cffd2399437f95b6cc85589778a3'
USER_ID = 'Chromecasting'  

# Initialize zeroconf and start discovery
def discover_chromecasts():
    zconf = zeroconf.Zeroconf()
    chromecasts = pychromecast.get_chromecasts(zconf)
    time.sleep(10)  # Allow some time for discovery
    zconf.close()
    devices = [cc.device.friendly_name for cc in chromecasts]
    print("Discovered Chromecast devices:", devices)  # Debugging statement
    return devices

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playlists', methods=['GET'])
def get_playlists():
    url = f"{JELLYFIN_ADDRESS}/Users/{USER_ID}/Items?IncludeItemTypes=Playlist&api_key={JELLYFIN_API}"
    headers = {'X-Emby-Token': JELLYFIN_API}
    response = requests.get(url, headers=headers)
    playlists = response.json().get('Items', [])
    return jsonify(playlists)

@app.route('/chromecasts', methods=['GET'])
def get_chromecasts():
    #devices = discover_chromecasts()
    devices = [
        "Master Bedroom speaker",
        "Serena speaker",
        "My TV",
        "Living Room Display",
        "Theo and Ollie speaker"
        ]
    response = jsonify(devices)
    response.headers.add('Content-Type', 'application/json')
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
    if items == '':
        print("nothing here")
    else:
        print(items)

    if not items:
        return jsonify({'status': 'error', 'message': 'No tracks found in playlist'}), 404
    
    # Get URL of the first item in the playlist
    media_url = f"{JELLYFIN_ADDRESS}/Audio/{items[0]['Id']}/stream.mp3?api_key={JELLYFIN_API}"

    # Find Chromecast device and connect
    chromecasts = pychromecast.get_chromecasts()
    device = next((cc for cc in chromecasts if cc.device.friendly_name == google_mini_name), None)
    if not device:
        return jsonify({'status': 'error', 'message': f"No Chromecast with name {google_mini_name} found"}), 404
    
    device.wait()

    # Cast media
    device.play_media(media_url, 'audio/mp3')
    device.block_until_active()

    return jsonify({'status': 'success', 'message': 'Your selection is playing on the selected Google Mini'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
