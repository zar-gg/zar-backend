function getPlayerData() {
    console.log("Getting player data")
    let url = `http://192.168.60.11:8000/get-player/${document.getElementById('player_name').value}?region=${document.getElementById('regions').value}`
    console.log(url)
    fetch(url)
    .then(response => response.json())
    .then(data => console.log(data));
};
