let search = document.getElementById('search')
let valid_search = document.getElementById('valid-search')

document.getElementById('formSearch').addEventListener('submit', function (e) {
    if (search.value == '') {
        e.preventDefault()
        valid_search.style.display = "block"
        valid_search.innerHTML = "Champs vide !"
    }
    else{
        valid_search.style.display = "none"
    }
})