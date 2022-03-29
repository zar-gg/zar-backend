function getPlayerDetails(){
    let params = (new URL(document.location)).searchParams;
    let name = document.getElementById('username').innerHTML
    let region = params.get("region");

    console.log(name, region)

    let url = `http://localhost:8000/get-player/${name}?region=${region}`

    fetch(url)
    .then(response => {
        console.log(response.status);
        if (response.status == 404){
            window.location.href = `http://localhost:8088/not-found`
        }
    })
    .then(data => {
        console.log(data);
    })
}
