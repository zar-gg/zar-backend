function getPlayerData() {
    if (document.getElementById('player_name').value.length > 0) {
    console.log("Getting player data")
    let url = `http://localhost:8000/get-players/${document.getElementById('player_name').value}?region=${document.getElementById('regions').value}`


    console.log(url)
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        
        const player_list_container = document.getElementById('player_list_container');
        const existing_list = document.getElementById('player_list_ul');
        const player_list = document.createElement('ul');
        
        player_list.classList.add('player_list_ul')
        player_list.id = 'player_list_ul'

        data.forEach((item) => {
            let li = document.createElement("li");
            li.innerHTML = `<div>
                                <span>
                                    <img id='profile_icon' src=${`static/ddragon/euw/12.5.1/img/profileicon/${item.profile_icon}.png`}>
                                    <text id='level'>${item.level}</text>
                                    <text id='name'>${item.name}</text>
                                </span>
                            </div>`
            li.classList.add('card')
            li.classList.add('playerCard')
            player_list.appendChild(li);
        });
        
        player_list_container.innerHTML
        
        if (existing_list == null){
            console.log('lel');
            player_list_container.appendChild(player_list);
        }
        else {
            console.log('replacing')
            player_list_container.replaceChild(player_list, existing_list);
        }
        

    });
}
};
