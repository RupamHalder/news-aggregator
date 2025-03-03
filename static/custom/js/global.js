import { CommonJsFunctions } from './globalFunctions.js';

$(document).ready(function () {
    const globalFunctions = new CommonJsFunctions();

    $('.multiSelect').select2();

    $(document).on('click', '.featureComingSoon', function () {
        globalFunctions.showCommingSoon();
    });
});
