function getPlayerDetails(){
    let params = (new URL(document.location)).searchParams;
    let name = document.getElementById('username').innerHTML
    let region = params.get("region");

    console.log(name, region)

    let url = `http://localhost:8000/get-player/${name}?region=${region}`

    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let player_details = document.getElementById('player_details')
        player_details.innerHTML = data
    });
}
