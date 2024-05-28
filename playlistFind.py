import requests

# Jellyfin configuration
JELLYFIN_ADDRESS = 'http://192.168.2.96:8096'
JELLYFIN_API = '6c81e0f1e3b044d38a326d95e6af74b9'
USER_ID = 'BenLang'  # Replace with the correct user ID

def get_playlists():
    url = f"{JELLYFIN_ADDRESS}/Users/{USER_ID}/Items"
    params = {
        'IncludeItemTypes': 'Playlist',
        'api_key': JELLYFIN_API
    }
    headers = {
        'X-Emby-Token': JELLYFIN_API
    }
    

    print(f"Requesting playlists from: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")

    response = requests.get(url, headers=headers, params=params)
    
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        playlists = response.json().get('Items', [])
        print("Fetched playlists:")
        for playlist in playlists:
            print(f"ID: {playlist['Id']}, Name: {playlist['Name']}")
        return playlists
    else:
        print(f"Failed to fetch playlists, status code: {response.status_code}, response: {response.text}")
        return []

if __name__ == "__main__":
    get_playlists()
