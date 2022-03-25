function getPlayerData() {
    if (document.getElementById("player_name_search").value.length > 0) {
        let url = `http://localhost:8000/get-players/${document.getElementById("player_name_search").value}?region=${document.getElementById("region_selector").value}`

        fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            
            const player_list_container = document.getElementById("player_list_container");
            
            let player_list_div = document.createElement("div")
            player_list_div.classList.add("player-list-div")
            player_list_div.id = "player_list_div"

            data.forEach((item) => {

                player_list_div.innerHTML += `<div class="col-lg-4">
                                                <div class="card shadow-lg player-card" onclick=gotoProfile(\`${item.name}\`);>
                                                    <div class="container">
                                                        <div class="row">
                                                            <div class="card-image col-md-4">
                                                                <img id="profile_icon" class="profile-icon" src=${`static/ddragon/euw/12.5.1/img/profileicon/${item.profile_icon}.png`}>
                                                            </div>
                                                            <div class="card-txt col-md-8">
                                                                <h4>${item.name}</h4>
                                                                <h6>Level: ${item.level}</h6>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>`
            });
            player_list_container.innerHTML = player_list_div.innerHTML;
        });
    }
    else {
        const player_list_container = document.getElementById("player_list_container");
        player_list_container.innerHTML = ''
    }
};

function gotoProfile(name){
    console.log(name, `${document.getElementById("region_selector").value}`)
    // document.cookie = `name=${name}; region=${document.getElementById("region_selector").value}; path=/;`
    // console.log(document.cookie)
    window.location.href = `http://localhost:8088/player-stats/${name}?region=${document.getElementById("region_selector").value}`
}

function searchProfile(){
    const name = document.getElementById("player_name_search").value
    window.location.href = `http://localhost:8088/player-stats/${name}?region=${document.getElementById("region_selector").value}`
}
