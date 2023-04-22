var username = document.getElementById("username");
var password = document.getElementById("password");
var button = document.getElementById("submit");
// "/[0-9]/g" &&& "/[A-z]/g"
var number = "admin";
var pattern = "tekV1z10n";
function validated() {
    if (username.value === '') {
        erroruser(username, 'Input is blank');
    }
    else if (username.value.match(number)) {
        correctuser(username, 'successfull');
    }
    else {
        erroruser(username, 'not match');
    }
    if (password.value === '') {
        errorpassword(password, 'Input is blank');
    }
    else if (password.value.match(pattern)) {
        correctpassword(password, 'successfull');
    }
    else {
        errorpassword(password, 'not match');

    }
    if (username.value.match(number) && password.value.match(pattern)) {
        window.location.href = "/index";
    }
}
function erroruser(input, text) {
    const checkuser = document.getElementById("user_error");
    checkuser.innerText = text;
}
function correctuser(input, textc) {
    const checkuser = document.getElementById("user_error");
    checkuser.innerText = textc;
}
function errorpassword(input, text) {
    const passerror = document.getElementById("pass_error");
    passerror.innerText = text;
}
function correctpassword(input, textp) {
    const checkpass = document.getElementById("pass_error");
    checkpass.innerText =textp;
}



