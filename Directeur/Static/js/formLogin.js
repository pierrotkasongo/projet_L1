let email = document.getElementById('email')
let valid_email = document.getElementById('valid-email')
let password = document.getElementById('password')
let valid_password = document.getElementById('valid-password')
let regexGmail = /^([a-zA-Z]+[0-9]{0,5}(\.[a-zA-Z]+)?[0-9]{0,5}@(gmail|icloud)+\.(com|fr))$/


document.getElementById('formLogin').addEventListener('submit', function (e) {
    if (email.value == '') {
        e.preventDefault()
        valid_email.style.display = 'block'
        valid_email.innerHTML = 'Champs vide !'
    }
    else if(!email.value.match(regexGmail)){
        e.preventDefault()
        valid_email.style.display = 'block'
        valid_email.innerHTML = 'Format invalide !'
    }
    else {
        valid_email.style.display = 'none'
    }

    if(password.value == ''){
        e.preventDefault()
        valid_password.style.display = 'block'
        valid_password.innerHTML = 'Champs vide !'
    }
    else {
        valid_password.style.display = 'none'
    }

})