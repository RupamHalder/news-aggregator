import { RegisterJsFunctions, CommonJsFunctions } from '../globalFunctions.js';

$(document).ready(function() {
    const registerFunctions = new RegisterJsFunctions();
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '.togglePassword', function(){
        globalFunctions.togglePasswordVisibility(this);
    });
});
