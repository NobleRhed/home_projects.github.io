from flask import Flask, render_template, request, jsonify
import pychromecast
import requests
import zeroconf
import time
import json


app = Flask(__name__)

# Jellyfin configuration
JELLYFIN_ADDRESS = 'http://192.168.2.96:8096'
JELLYFIN_API = '6c81e0f1e3b044d38a326d95e6af74b9'
USER_ID = 'ea92fcad0ab84419845c966d51a87838'  

@app.route('/')
def index():
    jf_address = JELLYFIN_ADDRESS
    return render_template('login.html', jf_address=jf_address)

@app.route('/chromecasts', methods=['GET'])
def get_chromecasts():
    try:
        with open('chromecast_devices.json', 'r') as f:
            devices = json.load(f)
        return jsonify(devices)
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'No Chromecast devices found'}), 404


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
    print(response.json())

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
    app.run(host='0.0.0.0', port=5003)
