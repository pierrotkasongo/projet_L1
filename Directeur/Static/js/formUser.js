let nom = document.getElementById("nom")
let valid_nom = document.getElementById("valid-nom")
let postnom = document.getElementById("postnom")
let valid_postnom = document.getElementById("valid-postnom")
let prenom = document.getElementById("prenom")
let valid_prenom = document.getElementById("valid-prenom")
let email = document.getElementById('email')
let valid_email = document.getElementById('valid-email')
let regexName = /^(^[a-zA-Z é è]+([-]?)+[a-zA-Z é è]+[ ]*)$/
let regexGmail = /^([a-zA-Z]+[0-9]{0,5}(\.[a-zA-Z]+)?[0-9]{0,5}@(gmail|icloud)+\.(com|fr))$/

document.getElementById('formUser').addEventListener('submit', function (e) {
    if (nom.value == "") {
        e.preventDefault()
        validationInputs(valid_nom, "Champs vide !")
    } else if (nom.value.length > 25) {
        e.preventDefault()
        validationInputs(valid_nom, "Trop long, maximum 25 caractères !")
    } else if (!nom.value.match(regexName)) {
        e.preventDefault()
        validationInputs(valid_nom, "Format invalide !")
    } else {
        valid_nom.style.display = "none"
    }

    if (postnom.value == "") {
        e.preventDefault()
        validationInputs(valid_postnom, "Champs vide !")
    } else if (postnom.value.length > 25) {
        e.preventDefault()
        validationInputs(valid_postnom, "Trop long, maximum 25 caractères !")
    } else if (!postnom.value.match(regexName)) {
        e.preventDefault()
        validationInputs(valid_postnom, "Format invalide !")
    } else {
        valid_postnom.style.display = "none"
    }

    if (prenom.value == "") {
        e.preventDefault()
        validationInputs(valid_prenom, "Champs vide !")
    } else if (prenom.value.length > 25) {
        e.preventDefault()
        validationInputs(valid_prenom, "Trop long, maximum 25 caractères !")
    } else if (!prenom.value.match(regexName)) {
        e.preventDefault()
        validationInputs(valid_prenom, "Format invalide !")
    } else {
        valid_prenom.style.display = "none"
    }

    if (email.value == "") {
        e.preventDefault()
        validationInputs(valid_email, "Champs vide !")
    }
    else if (email.value.length > 200) {
        e.preventDefault()
        validationInputs(valid_email, "Trop long, maximum 25 caractères !")
    }
    else if (!email.value.match(regexGmail)) {
        e.preventDefault()
        validationInputs(valid_email, "Format invalide !")
    }
    else {
        valid_email.style.display = "none"
    }
})



function validationInputs(check_input, message) {
    check_input.style.display = "block"
    check_input.innerHTML = message
    check_input.style.color = "red"
}  