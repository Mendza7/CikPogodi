//Autor: Mehmed Harcinovic 0261/19

const username = JSON.parse(document.getElementById('user_username').textContent);
const roomName = JSON.parse(document.getElementById('game_id').textContent);

var userData;
var napotezu;
var user; 
var remaining;
var lives = 6;
var pogadjanje;
var pogadjanje2;
var success = ""
var users;


//Async-AJAX poziv za dohvatanje informacija
async function getData(){
    return fetch(`http://${window.location.host}/game/get/ajax/${roomName}/`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
    .then(response=>response.json())
    .then(data=>{
        userData=data;
        console.log(data);
    });
}

//Ajax upit se ponavlja na 2 sekunde dok ne dodje drugi igrac
async function waitGame() {
    const data = await this.getData();
    console.log("ajax", userData)

    if(userData['user2']!==null) {
        updateNames();
        return;
    }
    else{
        setTimeout(waitGame, 2000);
        return;
    }
}

waitGame();

function updateNames(){
    console.log("usr",userData)
    if (username === userData['user1']){
        user = 0;
        tacna = userData['rec2'];
        opponent = userData['rec1'];

    }
    else if (username === userData['user2']){
        user = 1;
        tacna = userData['rec1'];
        opponent = userData['rec2'];

    }
    else return;
    remaining = tacna.length
    users =[userData['user1'],userData['user2']];

    pogadjanje = "_ ".repeat(tacna.length)
    let guess = document.getElementById("guessing1")
    guess.innerHTML = pogadjanje
    pogadjanje2 = "_ ".repeat(opponent.length)
    let guess2 = document.getElementById("guessing2")
    guess2.innerHTML = pogadjanje2

}



let url = `ws://${window.location.host}/ws/socket-server/game/${roomName}/`

const gameSocket = new WebSocket(url);

//Prijavljivanje serveru
gameSocket.onopen = ()=> gameSocket.send(JSON.stringify({
    'type':'initial',
    'username':username,
    'gameid':roomName
}))

gameSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    console.log("message received", data);
    let messages = document.getElementById('messages')

    switch (data['type']) {
        case 'players':
            if (userData['user1'] === data['user1'] && userData['first'] === 0) {
                napotezu = userData['user1'];
            } else {
                napotezu = userData['user2'];
            }
            console.log(napotezu)
            if(user === 0){
                document.getElementById('user1').innerHTML = userData['user1']
                document.getElementById('user2').innerHTML = userData['user2']
            }
            else{
                document.getElementById('user2').innerHTML = userData['user1']
                document.getElementById('user1').innerHTML = userData['user2']
            }

            break;
        case 'moveToClients':
            console.log("received toClient", data)
            if (username === data['username']) ;
            else {
                document.getElementById("guessing2").innerHTML = data['guessing']
                var elem = document.getElementById('lives62')
                elem.src = '/static/images/' + data['lives'] + '.png'
                napotezu = username;
            }
            break;
        case 'gameterm':
            alert(`Game over \n Winner: ${data['winner']}`);
            window.location.href = `http://${window.location.host}/izbor-rezima`
            break;
    }

//     messages.insertAdjacentHTML('beforeend',`<div>
//                                     <p>${JSON.stringify(data)}</p><br>
//                                 </div>`)
}


waitUser();


let form = document.getElementById("form")
form.addEventListener('submit',choose);

function choose(e){
    
   e.preventDefault()

   let message = e.target.tbInput.value

   var contains = false
   for (let i = 0; i < tacna.length; i++){
       if (success.includes(message))break;
       if(tacna[i] === message){
           contains = true
           pogadjanje = pogadjanje.substring(0,2*i) + message + pogadjanje.substring(2*i+1)
           document.getElementById("guessing1").innerHTML = pogadjanje
           remaining--
       }
   }

   if(success.includes(message)){
       napotezu = users[user];
       return;
   }
   else{
       if(contains===false) {
           lives--
           var elem = document.getElementById('lives61')
           elem.src = '/static/images/' + lives + '.png'
       }

       success = success + message
   }

   gameSocket.send(JSON.stringify({
       'type':'moveToServer',
       'rem':remaining,
       'username':username,
       'lives':lives,
       'letter':message,
       'guessing':pogadjanje,
       'word':tacna,
       'success':contains,
   }))


   document.getElementById(`btn${message}`).disabled = "disabled"

   form.reset()
   

   napotezu = users[1-user]
   waitUser();
}

function waitUser() {
    // console.log("user", username);
    // console.log("napotezu", napotezu);
    if(napotezu===username) {
        enableInput();
        return;
    }
    else{
        disableInput();
        setTimeout(waitUser, 50);
        return;
    }
    
}

function disableInput(){
    document.getElementById('tbInput').disabled = true;
    document.getElementById('dugme').disabled=true;
}

function enableInput(){
    document.getElementById('tbInput').disabled = false;
    document.getElementById('dugme').disabled=false;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}