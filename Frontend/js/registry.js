function checkRegistryData() {
    var data = new Array(4);
    data[0] = document.getElementsByName("email")[0].value;
    data[1] = document.getElementsByName("login")[0].value;
    data[2] = document.getElementsByName("first_password")[0].value;
    data[3] = document.getElementsByName("second_password")[0].value;
    
    var valid = true;
    if (data[0] == "" || data[1] == "" || data[2] == "" || data[3] == ""){
        alert("Одно из полей пустое. Попробуйте снова.");
        valid = false;
    }
    else if (data[2] != data[3]){
        alert("Пароли не совпадают. Попробуйте снова.");
        valid = false;
    }
    
    return valid;
}
