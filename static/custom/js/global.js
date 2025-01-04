import { CommonJsFunctions } from './globalFunctions.js';

$(document).ready(function () {
    const globalFunctions = new CommonJsFunctions();

    $(document).on('click', '.featureComingSoon', function () {
        globalFunctions.showCommingSoon();
    });
});
