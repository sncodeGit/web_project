function checkAuthData() {
    var data = new Array(2);
    data[0] = document.getElementsByName("login")[0].value;
    data[1] = document.getElementsByName("password")[0].value;
    
    if (data[0] == "" || data[1] == ""){
        alert("Одно из полей пустое. Попробуйте снова.");
    }
}
