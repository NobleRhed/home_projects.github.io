document.addEventListener('DOMContentLoaded', function() {
    const playlistSelect = document.getElementById('playlistSelect');
    const deviceSelect = document.getElementById('deviceSelect');
    const castButton = document.getElementById('castButton');

    // Fetch playlists from Flask server
    fetch('/playlists')
        .then(response => response.json())
        .then(data => {
            data.forEach(playlist => {
                const option = document.createElement('option');
                option.value = playlist.Id;
                option.textContent = playlist.Name;
                playlistSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching playlists:', error));

    // Fetch Chromecast devices from Flask server
    fetch('/chromecasts')
        .then(response => response.json())
        .then(data => {
            data.forEach(device => {
                const option = document.createElement('option');
                option.value = device;
                option.textContent = device;
                deviceSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching Chromecast devices:', error));

    // Handle cast button click
    castButton.addEventListener('click', function() {
        const selectedPlaylist = playlistSelect.value;
        const selectedDevice = deviceSelect.value;

        if (!selectedPlaylist || !selectedDevice) {
            alert('Please select both a playlist and a Chromecast device.');
            return;
        }

        const payload = {
            playlist_id: selectedPlaylist,
            google_mini_name: selectedDevice
        };

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
    });
});
