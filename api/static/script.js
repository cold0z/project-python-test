const codes = document.querySelectorAll('.code')
const email = document.getElementById("emailInput").value
const messageDiv = document.getElementById("message-retour")
const codeDiv = document.getElementById("codeContainer")



codes[0].focus()

codes.forEach((code, idx) => {
    code.addEventListener('keydown', (e) => {
        if(e.key >= 0 && e.key <=9) {
            codes[idx].value = ''
            setTimeout(() => codes[idx + 1].focus(), 10)
        } else if(e.key === 'Backspace') {
            setTimeout(() => codes[idx - 1].focus(), 10)
        }


        if(idx == 5){
            setTimeout(() => {
            var codePin = codes[0].value+codes[1].value+codes[2].value+codes[3].value+codes[4].value+codes[5].value;
            UserAction(email,codePin)
            }
            ,20)
        }
        
    })
    
    
})


function UserAction(email,code) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
             obj = JSON.parse(this.responseText)
             var message =obj.message;
             var className =obj.alert;
             messageDiv.innerHTML = message
             messageDiv.removeAttribute("class");
             messageDiv.classList.add(className);
             if(className == "success"){
                codeDiv.style.display ="none"
             }else{
                codeDiv.style.display ="default"
             }


         }
    };
    xhttp.open("POST", "http://127.0.0.1:5000//api/v1/auth/verify-code", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify( {'code':code,'email':email}));
}

