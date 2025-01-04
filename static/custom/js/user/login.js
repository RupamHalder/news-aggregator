import { LoginJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function() {
    const loginFunctions = new LoginJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '#togglePassword', function(){
        globalFunctions.togglePasswordVisibility(this);
    });
});
