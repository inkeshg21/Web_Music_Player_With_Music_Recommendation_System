
function showPassword(btnId, name) {
    var password = document.getElementsByName(name)
    var btn = document.getElementById(btnId)
    if (password[0].type === "password") {
        password[0].type = "text"
        btn.innerHTML = "<i class='fa-solid fa-eye-slash'></i>"
    }
    else if (password[0].type === "text") {
        password[0].type = "password"
        btn.innerHTML = "<i class='fa-solid fa-eye'></i>"
    }
}