const loginError = document.getElementById("login-error");

var forgottenPasswordSection = document.getElementById("forgotten-password-section");
var loginSection = document.getElementById("login-section")

var forgottenPasswordSection1 = document.getElementById("forgotten-password-section-1");
var forgottenPasswordSection2 = document.getElementById("forgotten-password-section-2");
var forgottenPasswordSection3 = document.getElementById("forgotten-password-section-3");

var emailValidationError = document.getElementById("email-validation-error");
var securityQuestionError = document.getElementById("security-question-error");

var securityQuestionContent = document.getElementById("security-question-content");

var eaToken = null;
var token = null;

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const callback = urlParams.get("callback")

window.addEventListener("load", () => {
    let value = localStorage.getItem("token");

    if (value != null) token = value;


    if ((window.location.pathname == "/login" || window.location.pathname == "/register") && token != null) {
        request("GET", `/api/authenticate-token?token=${token}`, null, (r) => {
            if (r.status == 200) window.location.replace("/dashboard")
            else {
                localStorage.removeItem("token");
                localStorage.removeItem("token-expiry");
            }
        })
    }
})

function login() {
    loginError.hidden = true;

    var email = document.getElementById("email-address").value;
    var password = document.getElementById("password").value;   

    if (email.length == 0) return alert("Please enter an email to continue.")
    if (password.length == 0) return alert("Please enter a password to continue.")

    request("GET", `/api/login?email=${email}&password=${password}`, null, (response) => {
        var payload = JSON.parse(response.responseText)

        console.log(response.status)

        if (response.status == 200) {
            localStorage.setItem("token", payload.token)
            localStorage.setItem("token-expiry", payload.expiry)

            if (callback == null ) window.location.replace("/dashboard")
            else window.location.replace(callback)

        } else {
            loginError.hidden = false;
        }
    })
}

function register() {
    var email = document.getElementById("email-address").value;
    var emailConfirm = document.getElementById("email-address-confirm").value;

    if (email.length == 0) return alert("Please enter an email address to continue.")
    else if (email != emailConfirm) return alert("Please ensure that the email addresses match.")

    var password = document.getElementById("password").value;   
    var passwordConfirm = document.getElementById("password-confirm").value;   

    if (password.length == 0) return alert("Please enter a password to continue.")
    else if (password != passwordConfirm) return alert("Please ensure that the passwords match.")

    var securityQuestion = document.getElementById("security-question").value;   
    var securityAnswer = document.getElementById("security-answer").value;   

    if (securityQuestion.length == 0) return alert("Please enter a security question to continue.")
    if (securityAnswer.length == 0) return alert("Please enter an answer to your security question to continue.")

    request("POST", `/api/register`, {"email": email, "password": password, "security-question": securityQuestion, "security-answer": securityAnswer}, (response) => {
        var payload = JSON.parse(response.responseText)

        if (response.status == 200) {
            localStorage.setItem("token", payload.token)
            localStorage.setItem("token-expiry", payload.expiry)

            if (callback == null ) window.location.replace("/dashboard")
            else window.location.replace(callback)

        } else {

        }
    })
}

function loadSecurityQuestion() {
    emailValidationError.hidden = true;
    var email = document.getElementById("email-address").value;

    if (email.length == 0) {
        emailValidationError.hidden = false;
        return;
    }

    request("GET", `/api/security-question?email=${email}`, null, (response) => {
        var payload = JSON.parse(response.responseText)

        if (response.status == 200) {
            securityQuestionContent.innerText = payload.question;

            forgottenPasswordSection1.hidden = true;
            forgottenPasswordSection2.hidden = false;
        } else {
            emailValidationError.hidden = false;
        }
    })

}

function validateSecurityQuestion() {
    var securityAnswer = document.getElementById("security-answer").value;
    var email = document.getElementById("email-address").value;

    securityQuestionError.hidden = true;

    if (securityAnswer.length == 0) return alert("Please enter a security answer to continue.")


    request("POST", `/api/security-question`, {"account-email": email, "security-answer": securityAnswer}, (response) => {
        var payload = JSON.parse(response.responseText)

        if (response.status == 200) {
            forgottenPasswordSection2.hidden = true;
            forgottenPasswordSection3.hidden = false;
            
            eaToken = payload.token;
        } else {
            securityQuestionError.hidden = false;
        }
    })
}

function toggleForgottenPassword() {
    forgottenPasswordSection.hidden = false;
    loginSection.hidden = true;

    forgottenPasswordSection1.hidden = false;
    forgottenPasswordSection2.hidden = true;
}

function toggleRememberPassword() {
    forgottenPasswordSection.hidden = true;
    loginSection.hidden = false;

    forgottenPasswordSection1.hidden = true;
    forgottenPasswordSection2.hidden = true;
}

function changePassword() {
    var password = document.getElementById("new-password").value;   
    var passwordConfirm = document.getElementById("new-password-confirm").value;   

    if (password.length == 0) return alert("Please enter a password to continue.")
    else if (password != passwordConfirm) return alert("Please ensure that the passwords match.")

    request("PUT", `/api/forgotten-password`, {"token": eaToken, "new-password": password}, (response) => {
        var payload = JSON.parse(response.responseText)

        if (response.status == 200) {
            localStorage.setItem("token", payload.token)
            localStorage.setItem("token-expiry", payload.expiry)

            if (callback == null ) window.location.replace("/dashboard")
            else window.location.replace(callback)

        } else {

        }
    })
}

function registerAccount() {
    let params = ""

    if (callback != null) params = `?callback=${encodeUrlParams(callback)}`

    window.location.replace(`/register${params}`)
}

function loginAccount() {
    let params = ""

    if (callback != null) params = `?callback=${encodeUrlParams(callback)}`

    window.location.replace(`/login${params}`)
}

function getToken() {
    return token;
}