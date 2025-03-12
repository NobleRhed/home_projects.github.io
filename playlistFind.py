#Purpose: This script is used to fetch playlists from Jellyfin server using Jellyfin API. Then using this detail, assigning the playlist to be sent to Chromecast device. NOTE: This script is not complete and is still in progress, HTTPS is mandatory for Jellyfin API, so need to figure out how to make requests to Jellyfin API using HTTPS.

# Importing the requests library for making HTTP requests
import requests


# Jellyfin configuration
JELLYFIN_ADDRESS = 'http://192.168.2.96:8096'
JELLYFIN_API = '6c81e0f1e3b044d38a326d95e6af74b9'
USER_ID = 'ea92fcad0ab84419845c966d51a87838'  # Replace with the correct user ID

# Function to fetch playlists from Jellyfin
def get_playlists():
    url = f"{JELLYFIN_ADDRESS}/Users/{USER_ID}/Items"
    # params here are instructing Jellyfin to only return playlists, and using the api key to authenticate
    params = {
        'IncludeItemTypes': 'Playlist',
        'api_key': JELLYFIN_API
    }
    # put the api key in the headers to authenticate
    headers = {
        'X-Emby-Token': JELLYFIN_API
    }
    

    print(f"Requesting playlists from: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")

    # response is what comes back from server
    response = requests.get(url, headers=headers, params=params)
    
    print(f"Response status code: {response.status_code}")
    # error handling for response, 200 is good
    if response.status_code == 200:
        playlists = response.json().get('Items', [])
        print("Fetched playlists:")
        for playlist in playlists:
            print(f"ID: {playlist['Id']}, Name: {playlist['Name']}")
        return playlists
    else:
        # if response is not 200, print error message TODO: add more error handling for not-found 404, not authorised 401 etc.
        print(f"Failed to fetch playlists, status code: {response.status_code}, response: {response.text}")
        return [] # return empty list if failed to fetch playlists

# Main function to run the script - this is new to me at the moment I was writing this script. This is used to determine if the current script is being run as the main program or if it is being imported as a module.
if __name__ == "__main__":
    get_playlists()
