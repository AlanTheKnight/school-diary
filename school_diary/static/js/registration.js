'use strict';

// regexes

let email = $("#email");
let emailregex = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
let myInput = document.getElementById("password1");
let letter = document.getElementById("letter");
let number = document.getElementById("number");
let length = document.getElementById("length");
let password1 = $("#password1");
let password2 = $("#password2");

myInput.onfocus = function() {
  document.getElementById("message").style.display = "block";
}

myInput.onblur = function() {
  document.getElementById("message").style.display = "none";
}

myInput.onkeyup = function() {
  let Letters = /[A-Za-zА-Яа-яЁё]+/;
  if(myInput.value.match(Letters)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
}

  let numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }

  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }
}

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
  if ((password1.val() == password2.val() && (password1.val().length > 0) && (password2.val().length > 0))) {
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

function emailCheck () {
  if (email.val().match(emailregex)) {
    setValid(email);
  } else {
    setInValid(email);
  }
}

function finalpasswordMatchCheck() {
  if ((password1.val() == password2.val() && (password1.val().length > 0) && (password2.val().length > 0))) {
    return true;
  }
  return false;
}

function finalpasswordCheck() {
  if (password1.val().match(/^(?=.*[0-9])[A-ZА-ЯЁ0-9!@#$%^&*_\-]{8,}$/i)) {
    return true;
  }
  return false;
}

function finalemailCheck () {
  if (email.val().match(emailregex)) {
    return true;
  }
  return false;
}

password2.on("input", passwordMatchCheck);
password1.on("input", passwordMatchCheck);
password1.on("input", passwordCheck);
email.on("input", emailCheck);

function validateMyForm() {
  console.log(finalemailCheck());
  console.log(finalpasswordMatchCheck());
  console.log(finalpasswordCheck());
  if ((finalemailCheck()) && (finalpasswordCheck) && finalpasswordMatchCheck()) {
    return true;
  } else {
    return false;
  }
 
}