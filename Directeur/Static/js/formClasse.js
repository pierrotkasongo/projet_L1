let classe = document.getElementById('classe')
let valid_classe = document.getElementById('valid-classe')
let regexClasse = /^[1-8]+[a-zA-Z è]+$/

document.getElementById('formClasse').addEventListener('submit', function (e) {
    if (classe.value == '') {
        e.preventDefault()
        valid_classe.style.display = "block"
        valid_classe.innerHTML = "Champs vide !"
    }
    else if (!classe.value.match(regexClasse)) {
        e.preventDefault()
        valid_classe.style.display = "block"
        valid_classe.innerHTML = "Format invalide !"
    }
    else{
        valid_classe.style.display = "none"
    }
})