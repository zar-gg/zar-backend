function getPlayerDetails(){
    let params = (new URL(document.location)).searchParams;
    let name = document.getElementById('username').innerHTML;
    let region = params.get("region");

    console.log(name, region);

    let url = `http://localhost:8000/get-player/${name}?region=${region}`

    fetch(url)
    .then(response => {
        console.log(response.status);
        if (response.status == 404){
            window.location.href = `http://localhost:8088/not-found`
        }
        return response.json()
    })
    .then(data => {
        console.log(data);

        let name = document.getElementById('name')
        let rank_info = document.getElementById('rank_info')
        let level = document.getElementById('level')
        let icon = document.getElementById('profile_icon')
        
        icon.src = `http://ddragon.leagueoflegends.com/cdn/12.10.1/img/profileicon/${data.iconId}.png`
        name.innerText = data.name
        level.innerText = data.level

        return data.enc_puuid
    })
    .then(puuid => {
        let url = `http://localhost:8000/match-history/${puuid}?region=${region}`
        
        fetch(url)
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log(data);
            // <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/champion/${item.player_details.championName}.png>
                                            
            let match_list_ul = document.createElement("ul")

            data.match_data.forEach((item) => {

            match_list_ul.innerHTML += ` <li>
                                            <img src=https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${item.player_details.championId}.png>
                                            <p>
                                                ${item.player_details.kills}/${item.player_details.deaths}/${item.player_details.assists}
                                            </p>
                                            <div>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item0}.png>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item1}.png>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item2}.png>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item3}.png>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item4}.png>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item5}.png>
                                                <img src=http://ddragon.leagueoflegends.com/cdn/12.10.1/img/item/${item.player_details.item6}.png>
                                            </div>
                                         </li>
                                         <hr>
                                        `
            });
            document.getElementById('match_history').innerHTML = match_list_ul.innerHTML
        });
    });
};
