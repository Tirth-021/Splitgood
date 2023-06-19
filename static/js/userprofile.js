const messageElement = document.querySelector('#js-message');
const message = document.querySelector('#message')
// Image elements
const fileUpload = document.querySelector('#js-file-uploader');
const profileTrigger = document.querySelector('#js-profile-trigger');
const profileBackground = document.querySelector('#js-profile-pic');

// Password objects
const password = document.querySelector('#js-password');
const password2 = document.querySelector('#js-password-new');
const passwordConfirm = document.querySelector('#js-password-confirm');
const passwordToggle = document.querySelector('#js-toggle-password');
const passwordToggle2 = document.querySelector('#js-toggle-password-new')
const passwordSuggest = document.querySelector('#js-suggest-password');
let passwordDisplayed = false;

// On form submission, check the passwords match and display a message if the password (would have) been saved.
document.querySelector('form').addEventListener('submit', function (event) {

    if (password2.value != passwordConfirm.value) {
        event.preventDefault();
        messageElement.innerText = 'The passwords don\'t match!';
        messageElement.classList.add('settings-message--error');
        messageElement.classList.remove('settings-message--success');
    }
});
function showMessage() {
    console.log('Inside JavaScript')
     if (message.value!=="") {
        messageElement.innerText = 'Wrong Password!';
        messageElement.classList.add('settings-message--error');
        messageElement.classList.remove('settings-message--success');
    }

}

// Trigger the file upload to set the profile picture
profileTrigger.addEventListener('click', function (event) {
    event.preventDefault();
    fileUpload.click();
});

// new profile pic added, display it
fileUpload.addEventListener("change", function (event) {
    document.getElementById("oldimage").style.visibility = "hidden";
    if (fileUpload.files && fileUpload.files[0]) {
        let reader = new FileReader();
        reader.onload = function (event) {
            // Remove the initial 'set picture image' text
            profileBackground.childNodes[0].nodeValue = "";
            // Set the new image src as the background
            profileBackground.style.backgroundImage = "url('" + event.target.result + "')";
        }
        reader.readAsDataURL(fileUpload.files[0]);
    }
});

// Add a suggested password for the user (to both password & confirm password inputs)
passwordSuggest.addEventListener('click', function (event) {
    let newPassword = btoa(Math.random().toString(36).substring(2));
    password2.value = newPassword;
    passwordConfirm.value = newPassword;
});

// Toggle the type of input the password field is (for user visibility)
passwordToggle.addEventListener('click', function (event) {
    passwordDisplayed = !passwordDisplayed;

    if (passwordDisplayed) {
        passwordToggle.innerText = "Hide Password";
        passwordConfirm.type = 'text';
        password.type = 'text';
    } else {
        passwordToggle.innerText = "Display Password";
        passwordConfirm.type = 'password';
        password.type = 'password';
    }
});

passwordToggle2.addEventListener('click', function (event) {
    passwordDisplayed = !passwordDisplayed;

    if (passwordDisplayed) {
        passwordToggle2.innerText = "Hide Password";
        passwordConfirm.type = 'text';
        password2.type = 'text';
    } else {
        passwordToggle2.innerText = "Display Password";
        passwordConfirm.type = 'password';
        password2.type = 'password';
    }
});