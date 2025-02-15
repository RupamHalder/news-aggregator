import { RegisterJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function () {
    const registerFunctions = new RegisterJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '.togglePassword', function () {
        globalFunctions.togglePasswordVisibility(this);
    });

    $(document).on('click', '#btnRegister', function () {
        let apiURL = '/api/v1/user/register';
        let method = 'POST';
        let data = JSON.stringify({
            email: $('#email').val(),
            password: $('#password').val(),
            conf_password: $('#conf_password').val()
        });
        let dataType = 'json';
        let processingButton = this;
        let postProcessing = () => {
            window.location.href = '/login';
        }
        let showSuccessMessage = true;
        globalFunctions.performPostAPICall(apiURL, method, data, dataType, processingButton, postProcessing, showSuccessMessage);
    });
});
