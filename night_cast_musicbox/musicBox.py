# Description: An attempt at getting jellyfin music to be included in another project as "playlists" for ifttt to trigger. DId not work, but will revisit this summer to see if it works using the reverse proxy method.

# Import flask, chromecast stuff, and other elements for web layer interaction
from flask import Flask, render_template, request, jsonify
import pychromecast
import requests
import json
import os

app = Flask(__name__)

# Jellyfin configuration
JELLYFIN_ADDRESS = 'http://192.168.2.96:8096'
JELLYFIN_API = '6c81e0f1e3b044d38a326d95e6af74b9'
USER_ID = 'ea92fcad0ab84419845c966d51a87838'

json_file_path = os.path.join(os.path.dirname(__file__), 'chromecast_devices.json')

# Load Chromecast devices from JSON file
with open(json_file_path, 'r') as f:
    chromecast_devices = json.load(f)

# routings. today (mar 12, 2025) we practiced using npm and node.js to route and use a personal database using a NoSQL. Take learned info during summer project to update this, and ensure it works. 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chromecasts')
def get_chromecasts():
    return jsonify(chromecast_devices)

@app.route('/cast', methods=['POST'])
def cast_playlist():
    data = request.form
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
    chromecast_name = next((device for device in chromecast_devices if device['friendly_name'] == google_mini_name), None)
    if not chromecast_name:
        return jsonify({'status': 'error', 'message': f"No Chromecast with name {google_mini_name} found"}), 404

    device = pychromecast.get_chromecast(friendly_name=chromecast_name['friendly_name'])
    device.wait()

    # Cast media 
    device.play_media(media_url, 'audio/mp3')
    device.block_until_active()

    # jsonify is crucial as browsers can only read strings, allowing for back and forth processing of data
    return jsonify({'status': 'success', 'message': 'Your selection is playing on the selected Google Mini'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)