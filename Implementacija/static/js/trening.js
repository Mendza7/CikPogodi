const username = JSON.parse(document.getElementById('user_username').textContent);
const roomName = JSON.parse(document.getElementById('trening_id').textContent);


let url = `ws://${window.location.host}/ws/socket-server/trening/${roomName}/`

var tacna  = JSON.parse(document.getElementById('recrec').textContent)
console.log("rec",tacna)
var remaining = tacna.length
var lives = 6
var pogadjanje = "_ ".repeat(tacna.length)
var success = ""
let guess = document.getElementById("guessing")
guess.innerHTML = pogadjanje

console.log('REC:',tacna)

const treningSocket = new WebSocket(url)

treningSocket.onopen = ()=> treningSocket.send(JSON.stringify({
    'type':'initial',
    'rec' :tacna,
    'username':username
}))

treningSocket.onmessage = function(e){
    let data = JSON.parse(e.data)

   console.log('Data:', data)

    if (data.type === 'result_msg'){
        let messages = document.getElementById('messages')

        messages.insertAdjacentHTML('beforeend',`<div>
                                        <p>${data.username} pokusao ${data.message} , rezultat: ${data.succ}, preostali broj zivota: ${data.lives}</p>
                                    </div>`)
    }
}

let form = document.getElementById("form")
form.addEventListener('submit',(e)=>{
   e.preventDefault()

   let message = e.target.tbInput.value

   var contains = false
   for (let i = 0; i < tacna.length; i++){
       if (success.includes(message))break;
       if(tacna[i] === message){
           contains = true
           pogadjanje = pogadjanje.substring(0,2*i) + message + pogadjanje.substring(2*i+1)
           document.getElementById("guessing").innerHTML = pogadjanje
           remaining--
       }
   }

   if(success.includes(message)){

   }
   else{
       if(contains===false) {
           lives--
           var elem = document.getElementById('lives6')
           elem.src = '/static/images/' + lives + '.png'
       }

       success = success + message
   }






   document.getElementById(`btn${message}`).disabled = "disabled"

   treningSocket.send(JSON.stringify({
        'type':'result_msg',
        'message': message,
        'username':username,
        'succ':(contains===true)?'uspeh':'neuspeh',
        'lives':lives
   }))

   if(lives===0){
       treningSocket.send(JSON.stringify({
           'type':'gameterm',
           'username':username,
           'lives':lives,
           'remaining':remaining
       }))
      alert("NEMATE VISE ZIVOTA")
       window.location.href =`http://${window.location.host}/izbor-rezima`
   }
   if(remaining===0){
       treningSocket.send(JSON.stringify({
           'type':'gameterm',
           'username':username,
           'lives':lives,
           'remaining':remaining
       }))
       alert("CESTITAMO!")
       window.location.href =`http://${window.location.host}/izbor-rezima`
   }


   form.reset()
})
