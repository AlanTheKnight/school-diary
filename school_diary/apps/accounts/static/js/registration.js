"use strict";

// regexes

let email = $("#id_email");
let emailRegex = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
let letter = $("#letter");
let number = $("#number");
let length = $("#length");
let password1 = $("#id_password1");
let password2 = $("#id_password2");

password1.on("focus", function () {
    $("#message").css("display", "block");
});

password1.on("blur", function () {
    $("#message").css("display", "none");
});

password1.on("keydown", function () {
    let Letters = /[A-Za-zА-Яа-яЁё]+/;
    if (password1.val().match(Letters)) {
        letter.removeClass("invalid");
        letter.addClass("valid");
    } else {
        letter.removeClass("valid");
        letter.addClass("invalid");
    }

    let numbers = /[0-9]/g;
    if (password1.val().match(numbers)) {
        number.removeClass("invalid");
        number.addClass("valid");
    } else {
        number.removeClass("valid");
        number.addClass("invalid");
    }

    if (password1.val().length >= 8) {
        length.removeClass("invalid");
        length.addClass("valid");
    } else {
        length.removeClass("valid");
        length.addClass("invalid");
    }
});

function setValid(el) {
    el.removeClass("is-invalid");
    el.removeClass("is-valid");
    el.addClass("is-valid");
}

function setInValid(el) {
    el.removeClass("is-valid");
    el.removeClass("is-invalid");
    el.addClass("is-invalid");
}

function passwordMatchCheck() {
    if (
        password1.val() === password2.val() &&
        password1.val().length > 0 &&
        password2.val().length > 0
    ) {
        setValid(password2);
    } else if (password2.val().length > 0) {
        setInValid(password2);
    }
}

function passwordCheck() {
    if (password1.val().match(/^(?=.*[0-9])[A-ZА-ЯЁ0-9!@#$%^&*_\-]{8,}$/i)) {
        setValid(password1);
    } else {
        setInValid(password1);
    }
}

function emailCheck() {
    if (email.val().match(emailRegex)) {
        setValid(email);
    } else {
        setInValid(email);
    }
}

function finalPasswordMatchCheck() {
    return (
        password1.val() === password2.val() &&
        password1.val().length > 0 &&
        password2.val().length > 0
    );
}

function finalPasswordCheck() {
    return password1.val().match(/^(?=.*[0-9])[A-ZА-ЯЁ0-9!@#$%^&*_\-]{8,}$/i);
}

function finalEmailCheck() {
    return email.val().match(emailRegex);
}

password2.on("input", passwordMatchCheck);
password1.on("input", passwordMatchCheck);
password1.on("input", passwordCheck);
email.on("input", emailCheck);

function validateMyForm() {
    return finalEmailCheck() && finalPasswordCheck && finalPasswordMatchCheck();
}

$(document).ready(function () {
    $("#show_hide_password a").on("click", function (event) {
        event.preventDefault();
        let passwordField = $("#id_password1");
        let hideBtnIcon = $("#show_hide_password i");
        if (passwordField.attr("type") === "text") {
            passwordField.attr("type", "password");
            hideBtnIcon.addClass("fa-eye-slash");
            hideBtnIcon.removeClass("fa-eye");
        } else {
            passwordField.attr("type", "text");
            hideBtnIcon.removeClass("fa-eye-slash");
            hideBtnIcon.addClass("fa-eye");
        }
    });
});
