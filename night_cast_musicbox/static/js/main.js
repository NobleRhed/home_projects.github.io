document.addEventListener('DOMContentLoaded', function() {
    fetch('/playlists')
        .then(response => response.json())
        .then(playlists => {
            const playlistsSelect = document.getElementById('playlists');
            playlists.forEach(playlist => {
                const option = document.createElement('option');
                option.value = playlist.Id;
                option.text = playlist.Name;
                playlistsSelect.appendChild(option);
            });
        });

    fetch('/chromecasts')
        .then(response => response.json())
        .then(chromecasts => {
            const chromecastsSelect = document.getElementById('chromecasts');
            chromecasts.forEach(device => {
                const option = document.createElement('option');
                option.value = device;
                option.text = device;
                chromecastsSelect.appendChild(option);
            });
        });

    document.getElementById('castForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const playlistId = document.getElementById('playlists').value;
        const chromecastName = document.getElementById('chromecasts').value;

        fetch('/cast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                playlist_id: playlistId,
                google_mini_name: chromecastName
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });
});
