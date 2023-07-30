let nom = document.getElementById("nom")
let valid_nom = document.getElementById("valid-nom")
let postnom = document.getElementById("postnom")
let valid_postnom = document.getElementById("valid-postnom")


document.getElementById('formUser').addEventListener('submit', function (e) {
    if (nom.value == "") {
        e.preventDefault()
        validationInputs(valid_nom, "Champs vide !")
    } else {
        valid_nom.style.display = "none"
    }

    if (postnom.value == "") {
        e.preventDefault()
        validationInputs(valid_postnom, "Champs vide !")
    } else {
        valid_postnom.style.display = "none"
    }
})



function validationInputs(check_input, message) {
    check_input.style.display = "block"
    check_input.innerHTML = message
    check_input.style.color = "red"
}  