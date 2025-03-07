document.addEventListener('DOMContentLoaded', function() {
    const playlistSelect = document.getElementById('playlistSelect');
    const deviceSelect = document.getElementById('deviceSelect');
    const castButton = document.getElementById('castButton');

    const accessToken = '{{ session["access_token"] }}';

    // Fetch Chromecast devices from Flask server
    fetch('/chromecasts')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch Chromecast devices');
            }
            return response.json();
        })
        .then(data => {
            console.log('Chromecast devices data:', data);
            if (!Array.isArray(data)) {
                throw new Error('Chromecast devices data is not an array');
            }
            data.forEach(device => {
                const option = document.createElement('option');
                option.value = device;
                option.textContent = device;
                deviceSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching Chromecast devices:', error));

    // Define the cast_playlist function
    function cast_playlist(playlist_id, google_mini_name) {
        const payload = {
            playlist_id: playlist_id,
            google_mini_name: google_mini_name
        };

        // Send request to cast playlist
        fetch('/cast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Your selection is playing on the selected Google Mini!');
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error('Error casting playlist:', error));
    }

    // Handle cast button click
    castButton.addEventListener('click', function() {
        const selectedPlaylist = playlistSelect.value;
        const selectedDevice = deviceSelect.value;

        if (!selectedPlaylist || !selectedDevice) {
            alert('Please select both a playlist and a Chromecast device.');
            return;
        }

        cast_playlist(selectedPlaylist, selectedDevice);
    });
});
