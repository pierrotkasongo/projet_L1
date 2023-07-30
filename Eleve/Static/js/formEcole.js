let ecole = document.getElementById('ecole')
let valid_ecole = document.getElementById('valid-ecole')
let regexEcole = /^(^[a-zA-Z è]+([-]?)+[a-zA-Z0-9 è]+[ ]*)$/

document.getElementById('formEcole').addEventListener('submit', function (e) {
    if (ecole.value == '') {
        e.preventDefault()
        valid_ecole.style.display = "block"
        valid_ecole.innerHTML = "Champs vide !"
    }
    else if (!ecole.value.match(regexEcole)) {
        e.preventDefault()
        valid_ecole.style.display = "block"
        valid_ecole.innerHTML = "Format invalide !"
    }
    else{
        valid_ecole.style.display = "none"
    }
})