import { LoginJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function() {
    const loginFunctions = new LoginJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '#togglePassword', function(){
        globalFunctions.togglePasswordVisibility(this);
    });

    $(document).on('click', '#btnUserLogin', function () {
        let apiURL = '/api/v1/user/login';
        let method = 'POST';
        let data = JSON.stringify({
            email: $('#email').val(),
            password: $('#password').val()
        });
        let dataType = 'json';
        let processingButton = this;
        let postProcessing = (responseData) => {
            if (responseData.home_page_redirection) {
                window.location.href = '/';
            }
        }
        let showSuccessMessage = true;
        globalFunctions.performPostAPICall(apiURL, method, data, dataType, processingButton, postProcessing, showSuccessMessage);
    });
});
